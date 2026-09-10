// =====================================================
// DARKTRACE INTEL — CINEMATIC INTRO
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", (event) => {
            event.preventDefault();

            const email = document.getElementById("email");
            const password = document.getElementById("password");

            if (!email.value.trim() || !password.value) {
                return;
            }

            if (!email.checkValidity()) {
                email.reportValidity();
                return;
            }

            window.location.href = "/app.html";
        });
    }

    // =================================================
    // CINEMATIC FIRST-LOAD INTRO
    // =================================================

    const intro = document.getElementById("introScreen");
    const progress = document.getElementById("introProgress");
    const percent = document.getElementById("introPercent");
    const status = document.getElementById("introStatus");
    const log = document.getElementById("introLog");

    // Agar intro HTML mein available nahi hai,
    // to page normally chalega.
    if (intro && progress && percent && status && log) {

        document.body.classList.add("intro-active");

        const stages = [
            [
                "INITIALIZING SYSTEM",
                "ENCRYPTED CHANNEL // READY"
            ],
            [
                "ESTABLISHING SECURE CHANNEL",
                "SECURITY LAYER // CONNECTED"
            ],
            [
                "ANALYZING THREAT NETWORK",
                "INTELLIGENCE NODES // ONLINE"
            ],
            [
                "LOADING AI ENGINE",
                "AI CORE // READY"
            ],
            [
                "SYSTEM READY",
                "DARKTRACE // ACCESS GRANTED"
            ]
        ];

        let value = 0;
        let stageIndex = 0;

        const introTimer = setInterval(() => {

            // Random progress
            value += Math.floor(Math.random() * 7) + 3;

            // Maximum 100%
            if (value >= 100) {

                value = 100;

                clearInterval(introTimer);

                status.textContent = "SYSTEM READY";
                log.textContent = "DARKTRACE // ACCESS GRANTED";

                progress.style.width = "100%";
                percent.textContent = "100%";

                // Short pause after 100%
                setTimeout(() => {

                    intro.classList.add("is-leaving");

                    document.body.classList.remove("intro-active");

                    // Remove intro completely
                    setTimeout(() => {
                        intro.remove();
                    }, 950);

                }, 500);

                return;
            }

            // Determine current stage
            const newStage = Math.min(
                stages.length - 1,
                Math.floor(value / 22)
            );

            // Change text when stage changes
            if (newStage !== stageIndex) {

                stageIndex = newStage;

                status.textContent =
                    stages[stageIndex][0];

                log.textContent =
                    stages[stageIndex][1];
            }

            // Update progress bar
            progress.style.width = `${value}%`;

            // Update percentage
            percent.textContent =
                `${String(value).padStart(2, "0")}%`;

        }, 115);
    }

});