import os
import asyncio
import threading
import traceback

from flask import Flask, render_template
from flask_sock import Sock
from dotenv import load_dotenv

from phonic import AsyncPhonic, AudioChunkPayload
from phonic.types.config_payload import ConfigPayload


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


PHONIC_API_KEY = os.getenv("PHONIC_API_KEY")
PHONIC_PROJECT = os.getenv("PHONIC_PROJECT", "main")
PHONIC_AGENT = os.getenv(
    "PHONIC_AGENT",
    "hindi-web-agent",
)

HOST = os.getenv(
    "HOST",
    "127.0.0.1",
)

PORT = int(
    os.getenv(
        "PORT",
        "8000",
    )
)


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)
sock = Sock(app)


# ============================================================
# PHONIC CLIENT
# ============================================================

phonic_client = AsyncPhonic(
    api_key=PHONIC_API_KEY
)


# ============================================================
# CONFIGURATION
# ============================================================

print("=" * 60)
print("PHONIC HINDI VOICE AGENT")
print("=" * 60)

print(
    "Phonic API key:",
    "loaded" if PHONIC_API_KEY else "MISSING",
)

print(
    "Phonic project:",
    PHONIC_PROJECT,
)

print(
    "Phonic agent:",
    PHONIC_AGENT,
)

print(
    "Host:",
    HOST,
)

print(
    "Port:",
    PORT,
)

print("=" * 60)


# ============================================================
# FRONTEND
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# HEALTH
# ============================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "project": PHONIC_PROJECT,
        "agent": PHONIC_AGENT,
    }


# ============================================================
# PHONIC SESSION
# ============================================================

async def phonic_session(
    browser_ws,
    audio_queue,
):

    socket = None

    try:

        print()
        print("=" * 60)
        print("PHONIC CONNECTING")
        print("=" * 60)

        # ----------------------------------------------------
        # CONNECT TO PHONIC
        # ----------------------------------------------------

        async with phonic_client.conversations.connect() as socket:

            print(
                "Phonic WebSocket connected"
            )

            # ------------------------------------------------
            # PHONIC MESSAGE HANDLER
            # ------------------------------------------------

            async def on_phonic_message(
                message
            ):

                try:

                    message_type = getattr(
                        message,
                        "type",
                        None,
                    )

                    print(
                        "[PHONIC]",
                        message_type,
                    )

                    # ----------------------------------------
                    # AUDIO FROM PHONIC
                    # ----------------------------------------

                    if message_type == "audio_chunk":

                        audio = getattr(
                            message,
                            "audio",
                            None,
                        )

                        if audio:

                            browser_ws.send(
                                '{"type":"audio","audio":"'
                                + audio
                                + '"}'
                            )

                        return

                    # ----------------------------------------
                    # OTHER PHONIC EVENTS
                    # ----------------------------------------

                    try:

                        data = message.model_dump(
                            mode="json"
                        )

                    except Exception:

                        data = {
                            "type": message_type,
                            "message": str(
                                message
                            ),
                        }

                    print(
                        "[PHONIC EVENT]",
                        data,
                    )

                    # Send event to browser
                    import json

                    browser_ws.send(
                        json.dumps(
                            {
                                "type": "phonic_event",
                                "data": data,
                            }
                        )
                    )

                except Exception as error:

                    print(
                        "[PHONIC MESSAGE ERROR]",
                        error,
                    )

                    traceback.print_exc()


            # ------------------------------------------------
            # REGISTER HANDLER
            # ------------------------------------------------

            socket.on(
                "message",
                on_phonic_message,
            )

            # ------------------------------------------------
            # START PHONIC LISTENER
            # ------------------------------------------------

            asyncio.create_task(
                socket.start_listening()
            )

            # ------------------------------------------------
            # SEND CONFIGURATION
            # ------------------------------------------------

            config = ConfigPayload(
                agent=PHONIC_AGENT,
                project=PHONIC_PROJECT,
                input_format="pcm_16000",
                output_format="pcm_16000",
            )

            print()
            print(
                "Sending Phonic configuration..."
            )

            print(
                config
            )

            await socket.send_config(
                config
            )

            print(
                "Phonic configuration sent"
            )

            # ------------------------------------------------
            # TELL BROWSER
            # ------------------------------------------------

            import json

            browser_ws.send(
                json.dumps(
                    {
                        "type": "connected",
                        "message": "Phonic connected",
                    }
                )
            )

            # ------------------------------------------------
            # AUDIO FORWARDING LOOP
            # ------------------------------------------------

            while True:

                audio_data = await audio_queue.get()

                if audio_data is None:

                    break

                try:

                    # IMPORTANT:
                    # The Phonic Python SDK expects
                    # AudioChunkPayload.

                    if isinstance(
                        audio_data,
                        AudioChunkPayload,
                    ):

                        chunk = audio_data

                    else:

                        chunk = AudioChunkPayload(
                            audio=audio_data
                        )

                    await socket.send_audio_chunk(
                        chunk
                    )

                except Exception as error:

                    print()
                    print(
                        "Phonic audio send error:",
                        error,
                    )

                    traceback.print_exc()

                    break

    except Exception as error:

        print()
        print("=" * 60)
        print("PHONIC SESSION ERROR")
        print("=" * 60)

        print(
            "Type:",
            type(error).__name__,
        )

        print(
            "Error:",
            error,
        )

        traceback.print_exc()

        try:

            import json

            browser_ws.send(
                json.dumps(
                    {
                        "type": "server_error",
                        "error": str(error),
                    }
                )
            )

        except Exception:
            pass

    finally:

        print(
            "Phonic session closed"
        )


# ============================================================
# BROWSER WEBSOCKET
# ============================================================

@sock.route("/ws")
def websocket():

    print()
    print("=" * 60)
    print("BROWSER WEBSOCKET CONNECTED")
    print("=" * 60)

    # --------------------------------------------------------
    # IMPORTANT
    # Flask-Sock handler is synchronous.
    # Phonic SDK is asynchronous.
    #
    # We create a dedicated asyncio event loop.
    # --------------------------------------------------------

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(
        loop
    )

    audio_queue = asyncio.Queue()

    phonic_task = None

    try:

        # ----------------------------------------------------
        # Start Phonic session
        # ----------------------------------------------------

        # Flask-Sock's ws object is synchronous,
        # so pass it to the async session.

        phonic_task = loop.create_task(
            phonic_session(
                websocket,
                audio_queue,
            )
        )

        # ----------------------------------------------------
        # Browser message loop
        # ----------------------------------------------------

        while True:

            message = websocket.receive()

            if message is None:

                print(
                    "Browser WebSocket closed"
                )

                break

            # ------------------------------------------------
            # Browser sends JSON text
            # ------------------------------------------------

            if isinstance(
                message,
                str,
            ):

                import json

                try:

                    data = json.loads(
                        message
                    )

                except Exception:

                    print(
                        "Invalid browser JSON"
                    )

                    continue

                message_type = data.get(
                    "type"
                )

                # --------------------------------------------
                # HELLO
                # --------------------------------------------

                if message_type == "hello":

                    websocket.send(
                        json.dumps(
                            {
                                "type": "hello",
                                "message": "Server ready",
                            }
                        )
                    )

                    continue

                # --------------------------------------------
                # AUDIO
                # --------------------------------------------

                if message_type == "audio":

                    audio = data.get(
                        "audio"
                    )

                    if audio:

                        # Queue audio into
                        # asyncio loop.

                        asyncio.run_coroutine_threadsafe(
                            audio_queue.put(
                                AudioChunkPayload(
                                    audio=audio
                                )
                            ),
                            loop,
                        )

                    continue

                # --------------------------------------------
                # STOP
                # --------------------------------------------

                if message_type == "stop":

                    print(
                        "Browser requested stop"
                    )

                    break

                # --------------------------------------------
                # PING
                # --------------------------------------------

                if message_type == "ping":

                    websocket.send(
                        json.dumps(
                            {
                                "type": "pong"
                            }
                        )
                    )

                    continue

    except Exception as error:

        print()
        print(
            "=" * 60
        )
        print(
            "BROWSER WEBSOCKET ERROR"
        )
        print(
            "=" * 60
        )

        print(
            type(error).__name__,
            error,
        )

        traceback.print_exc()

    finally:

        # ----------------------------------------------------
        # Tell Phonic session to stop
        # ----------------------------------------------------

        try:

            asyncio.run_coroutine_threadsafe(
                audio_queue.put(None),
                loop,
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # Finish Phonic task
        # ----------------------------------------------------

        try:

            if phonic_task:

                loop.run_until_complete(
                    phonic_task
                )

        except Exception as error:

            print(
                "Phonic task close error:",
                error,
            )

        # ----------------------------------------------------
        # Close event loop
        # ----------------------------------------------------

        try:

            loop.stop()
            loop.close()

        except Exception:
            pass

        print(
            "Browser session cleaned up"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("STARTING FLASK SERVER")
    print("=" * 60)

    print(
        f"http://{HOST}:{PORT}"
    )

    print("=" * 60)

    app.run(
        host=HOST,
        port=PORT,
        debug=False,
        threaded=True,
    )