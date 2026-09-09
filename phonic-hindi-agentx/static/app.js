let socket = null;

let running = false;

let microphoneStarted = false;


const startButton =
    document.getElementById(
        "startButton"
    );


const stopButton =
    document.getElementById(
        "stopButton"
    );


const statusText =
    document.getElementById(
        "statusText"
    );


const statusDot =
    document.getElementById(
        "statusDot"
    );


const logElement =
    document.getElementById(
        "log"
    );


const conversationElement =
    document.getElementById(
        "conversation"
    );


// ==========================================================
// LOG
// ==========================================================

function log(message) {

    const now =
        new Date()
            .toLocaleTimeString();


    logElement.textContent +=
        `[${now}] ${message}\n`;


    logElement.scrollTop =
        logElement.scrollHeight;
}


// ==========================================================
// STATUS
// ==========================================================

function setStatus(
    text,
    connected
) {

    statusText.textContent =
        text;


    if (connected) {

        statusDot.classList.add(
            "connected"
        );

    } else {

        statusDot.classList.remove(
            "connected"
        );
    }
}


// ==========================================================
// CONVERSATION
// ==========================================================

function addConversation(
    text
) {

    if (!text) {
        return;
    }


    if (
        conversationElement.textContent.trim() ===
        "Press \"Start Conversation\" and speak Hindi."
    ) {

        conversationElement.textContent =
            "";
    }


    conversationElement.textContent +=
        text +
        "\n";


    conversationElement.scrollTop =
        conversationElement.scrollHeight;
}


// ==========================================================
// START
// ==========================================================

async function startConversation() {

    if (running) {
        return;
    }


    running = true;


    startButton.disabled =
        true;


    stopButton.disabled =
        false;


    log(
        "Starting Hindi voice assistant..."
    );


    try {

        // --------------------------------------------------
        // WebSocket URL
        // --------------------------------------------------

        const protocol =
            window.location.protocol ===
            "https:"
                ? "wss:"
                : "ws:";


        const wsUrl =
            `${protocol}//${window.location.host}/ws`;


        log(
            `Connecting to ${wsUrl}`
        );


        socket =
            new WebSocket(
                wsUrl
            );


        // --------------------------------------------------
        // OPEN
        // --------------------------------------------------

        socket.onopen =
            async () => {

                log(
                    "Browser WebSocket connected"
                );


                setStatus(
                    "Connected",
                    true
                );


                socket.send(
                    JSON.stringify({
                        type: "hello"
                    })
                );


                // ------------------------------------------
                // Start microphone
                // ------------------------------------------

                try {

                    await startMicrophone(
                        (base64Audio) => {

                            if (
                                socket &&
                                socket.readyState ===
                                WebSocket.OPEN
                            ) {

                                socket.send(
                                    JSON.stringify({
                                        type: "audio",
                                        audio: base64Audio
                                    })
                                );
                            }
                        }
                    );


                    microphoneStarted =
                        true;


                    log(
                        "Microphone started"
                    );


                    setStatus(
                        "Listening",
                        true
                    );

                } catch (error) {

                    log(
                        `Microphone error: ${error.message}`
                    );


                    stopConversation();
                }
            };


        // --------------------------------------------------
        // MESSAGE
        // --------------------------------------------------

        socket.onmessage =
            async (event) => {

                let data;


                try {

                    data =
                        JSON.parse(
                            event.data
                        );

                } catch (error) {

                    log(
                        "Invalid server message"
                    );

                    return;
                }


                // ------------------------------------------
                // Server ready
                // ------------------------------------------

                if (
                    data.type ===
                    "server_ready"
                ) {

                    log(
                        data.message ||
                        "Server ready"
                    );

                    return;
                }


                // ------------------------------------------
                // Phonic connected
                // ------------------------------------------

                if (
                    data.type ===
                    "connected"
                ) {

                    log(
                        "Phonic connected"
                    );


                    setStatus(
                        "Phonic connected",
                        true
                    );


                    return;
                }


                // ------------------------------------------
                // Hello
                // ------------------------------------------

                if (
                    data.type ===
                    "hello"
                ) {

                    log(
                        data.message ||
                        "Server ready"
                    );

                    return;
                }


                // ------------------------------------------
                // Audio
                // ------------------------------------------

                if (
                    data.type ===
                    "audio"
                ) {

                    if (
                        data.audio
                    ) {

                        await playPCM16(
                            data.audio,
                            16000
                        );
                    }


                    return;
                }


                // ------------------------------------------
                // Transcript
                // ------------------------------------------

                if (
                    data.type ===
                    "transcript"
                ) {

                    if (
                        data.text
                    ) {

                        addConversation(
                            "आप: " +
                            data.text
                        );
                    }


                    return;
                }


                // ------------------------------------------
                // Phonic event
                // ------------------------------------------

                if (
                    data.type ===
                    "phonic_event"
                ) {

                    const eventData =
                        data.data ||
                        {};


                    const eventType =
                        eventData.type ||
                        "unknown";


                    log(
                        `Phonic event: ${eventType}`
                    );


                    // Show useful text
                    if (
                        eventData.text
                    ) {

                        addConversation(
                            eventData.text
                        );
                    }


                    // Error
                    if (
                        eventType ===
                        "error"
                    ) {

                        log(
                            `Phonic error: ${
                                JSON.stringify(
                                    eventData
                                )
                            }`
                        );
                    }


                    return;
                }


                // ------------------------------------------
                // Server error
                // ------------------------------------------

                if (
                    data.type ===
                    "server_error"
                ) {

                    log(
                        `Server error: ${data.error}`
                    );


                    setStatus(
                        "Error",
                        false
                    );


                    return;
                }


                // ------------------------------------------
                // Pong
                // ------------------------------------------

                if (
                    data.type ===
                    "pong"
                ) {

                    return;
                }
            };


        // --------------------------------------------------
        // ERROR
        // --------------------------------------------------

        socket.onerror =
            (error) => {

                console.error(
                    error
                );


                log(
                    "WebSocket error"
                );


                setStatus(
                    "Connection error",
                    false
                );
            };


        // --------------------------------------------------
        // CLOSE
        // --------------------------------------------------

        socket.onclose =
            () => {

                log(
                    "WebSocket closed"
                );


                cleanup();
            };
    }


    catch (error) {

        log(
            `Start error: ${error.message}`
        );


        cleanup();
    }
}


// ==========================================================
// STOP
// ==========================================================

function stopConversation() {

    if (!running) {
        return;
    }


    log(
        "Stopping conversation..."
    );


    running = false;


    // ------------------------------------------------------
    // Microphone
    // ------------------------------------------------------

    if (
        microphoneStarted
    ) {

        try {

            stopMicrophone();

        } catch (error) {

            console.error(
                error
            );
        }


        microphoneStarted =
            false;
    }


    // ------------------------------------------------------
    // Browser WebSocket
    // ------------------------------------------------------

    if (
        socket &&
        socket.readyState ===
        WebSocket.OPEN
    ) {

        try {

            socket.send(
                JSON.stringify({
                    type: "stop"
                })
            );

        } catch (error) {

            console.error(
                error
            );
        }


        setTimeout(
            () => {

                if (
                    socket &&
                    socket.readyState !==
                    WebSocket.CLOSED
                ) {

                    socket.close();
                }

            },
            100
        );
    }


    else if (
        socket
    ) {

        socket.close();
    }


    socket =
        null;


    cleanup();
}


// ==========================================================
// CLEANUP
// ==========================================================

function cleanup() {

    running =
        false;


    microphoneStarted =
        false;


    startButton.disabled =
        false;


    stopButton.disabled =
        true;


    setStatus(
        "Disconnected",
        false
    );
}


// ==========================================================
// BUTTONS
// ==========================================================

startButton.addEventListener(
    "click",
    startConversation
);


stopButton.addEventListener(
    "click",
    stopConversation
);