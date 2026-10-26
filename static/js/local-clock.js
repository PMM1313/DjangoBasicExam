

document.addEventListener("DOMContentLoaded", function () {
    const clock = document.getElementById("local-time");

    if (!clock) {
        return;
    }

    function updateClock() {
        const now = new Date();

        clock.textContent = new Intl.DateTimeFormat("en-GB", {
            timeZone: "Europe/Sofia",
            day: "2-digit",
            month: "long",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
        }).format(now);
    }

    updateClock();
    setInterval(updateClock, 1000);
});

