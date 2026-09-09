class AudioManager {

    constructor() {

        this.audioContext = null;

        this.mediaStream = null;

        this.source = null;

        this.processor = null;

        this.isRecording = false;

        this.targetSampleRate = 16000;

        this.onAudioData = null;

        this.playbackContext = null;
    }


    // ========================================================
    // START MICROPHONE
    // ========================================================

    async startMicrophone(callback) {

        this.onAudioData = callback;


        this.mediaStream =
            await navigator.mediaDevices.getUserMedia({
                audio: {
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                },
                video: false
            });


        this.audioContext =
            new (
                window.AudioContext ||
                window.webkitAudioContext
            )();


        if (
            this.audioContext.state ===
            "suspended"
        ) {

            await this.audioContext.resume();
        }


        this.source =
            this.audioContext.createMediaStreamSource(
                this.mediaStream
            );


        this.processor =
            this.audioContext.createScriptProcessor(
                4096,
                1,
                1
            );


        this.processor.onaudioprocess =
            (event) => {

                if (!this.isRecording) {
                    return;
                }


                const input =
                    event.inputBuffer
                        .getChannelData(0);


                const resampled =
                    this.resample(
                        input,
                        this.audioContext.sampleRate,
                        this.targetSampleRate
                    );


                const pcm =
                    this.convertToPCM16(
                        resampled
                    );


                const base64 =
                    this.uint8ToBase64(
                        pcm
                    );


                if (
                    this.onAudioData
                ) {

                    this.onAudioData(
                        base64
                    );
                }
            };


        this.source.connect(
            this.processor
        );


        this.processor.connect(
            this.audioContext.destination
        );


        this.isRecording = true;


        console.log(
            "Microphone started"
        );
    }


    // ========================================================
    // RESAMPLE
    // ========================================================

    resample(
        input,
        inputRate,
        outputRate
    ) {

        if (
            inputRate ===
            outputRate
        ) {

            return input;
        }


        const ratio =
            inputRate /
            outputRate;


        const outputLength =
            Math.floor(
                input.length /
                ratio
            );


        const output =
            new Float32Array(
                outputLength
            );


        for (
            let i = 0;
            i < outputLength;
            i++
        ) {

            const position =
                i * ratio;


            const index =
                Math.floor(
                    position
                );


            const fraction =
                position -
                index;


            const sample1 =
                input[index] || 0;


            const sample2 =
                input[index + 1] || sample1;


            output[i] =
                sample1 +
                (
                    sample2 -
                    sample1
                ) *
                fraction;
        }


        return output;
    }


    // ========================================================
    // FLOAT32 -> PCM16
    // ========================================================

    convertToPCM16(input) {

        const buffer =
            new ArrayBuffer(
                input.length * 2
            );


        const view =
            new DataView(
                buffer
            );


        for (
            let i = 0;
            i < input.length;
            i++
        ) {

            let sample =
                Math.max(
                    -1,
                    Math.min(
                        1,
                        input[i]
                    )
                );


            let value;


            if (
                sample < 0
            ) {

                value =
                    sample *
                    0x8000;

            } else {

                value =
                    sample *
                    0x7FFF;
            }


            view.setInt16(
                i * 2,
                value,
                true
            );
        }


        return new Uint8Array(
            buffer
        );
    }


    // ========================================================
    // UINT8 -> BASE64
    // ========================================================

    uint8ToBase64(bytes) {

        let binary = "";

        const chunkSize = 0x8000;


        for (
            let i = 0;
            i < bytes.length;
            i += chunkSize
        ) {

            const chunk =
                bytes.subarray(
                    i,
                    Math.min(
                        i + chunkSize,
                        bytes.length
                    )
                );


            binary += String.fromCharCode(
                ...chunk
            );
        }


        return btoa(
            binary
        );
    }


    // ========================================================
    // BASE64 -> UINT8
    // ========================================================

    base64ToUint8(base64) {

        const binary =
            atob(base64);


        const bytes =
            new Uint8Array(
                binary.length
            );


        for (
            let i = 0;
            i < binary.length;
            i++
        ) {

            bytes[i] =
                binary.charCodeAt(i);
        }


        return bytes;
    }


    // ========================================================
    // PLAY PCM16
    // ========================================================

    async playPCM16(
        base64Audio,
        sampleRate = 16000
    ) {

        try {

            if (
                !this.playbackContext
            ) {

                this.playbackContext =
                    new (
                        window.AudioContext ||
                        window.webkitAudioContext
                    )();
            }


            if (
                this.playbackContext.state ===
                "suspended"
            ) {

                await this.playbackContext.resume();
            }


            const pcm =
                this.base64ToUint8(
                    base64Audio
                );


            const sampleCount =
                Math.floor(
                    pcm.length / 2
                );


            const audioBuffer =
                this.playbackContext.createBuffer(
                    1,
                    sampleCount,
                    sampleRate
                );


            const channel =
                audioBuffer.getChannelData(
                    0
                );


            const view =
                new DataView(
                    pcm.buffer,
                    pcm.byteOffset,
                    pcm.byteLength
                );


            for (
                let i = 0;
                i < sampleCount;
                i++
            ) {

                channel[i] =
                    view.getInt16(
                        i * 2,
                        true
                    ) / 32768;
            }


            const source =
                this.playbackContext
                    .createBufferSource();


            source.buffer =
                audioBuffer;


            source.connect(
                this.playbackContext.destination
            );


            source.start();

        } catch (error) {

            console.error(
                "Audio playback error:",
                error
            );
        }
    }


    // ========================================================
    // STOP
    // ========================================================

    stopMicrophone() {

        this.isRecording = false;


        if (
            this.processor
        ) {

            this.processor.disconnect();

            this.processor = null;
        }


        if (
            this.source
        ) {

            this.source.disconnect();

            this.source = null;
        }


        if (
            this.mediaStream
        ) {

            this.mediaStream
                .getTracks()
                .forEach(
                    track =>
                        track.stop()
                );

            this.mediaStream = null;
        }


        if (
            this.audioContext
        ) {

            this.audioContext.close();

            this.audioContext = null;
        }


        console.log(
            "Microphone stopped"
        );
    }


    // ========================================================
    // STOP EVERYTHING
    // ========================================================

    stop() {

        this.stopMicrophone();


        if (
            this.playbackContext
        ) {

            this.playbackContext.close();

            this.playbackContext = null;
        }
    }
}


// ============================================================
// GLOBAL
// ============================================================

window.audioManager =
    new AudioManager();


window.startMicrophone =
    async function(callback) {

        return window.audioManager
            .startMicrophone(
                callback
            );
    };


window.stopMicrophone =
    function() {

        window.audioManager
            .stopMicrophone();
    };


window.playPCM16 =
    async function(
        base64Audio,
        sampleRate = 16000
    ) {

        return window.audioManager
            .playPCM16(
                base64Audio,
                sampleRate
            );
    };