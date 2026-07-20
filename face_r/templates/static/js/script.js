```javascript
// ----------------------------
// Live Dashboard Update
// ----------------------------

function updateStats() {

    fetch("/stats")
        .then(response => response.json())
        .then(data => {

            document.getElementById("faces").innerHTML = data.faces;
            document.getElementById("fps").innerHTML = data.fps;
            document.getElementById("status").innerHTML = data.status;
            document.getElementById("distance").innerHTML = data.distance;
            document.getElementById("time").innerHTML = data.time;

            // Status Color
            if (data.status === "Face Detected") {

                document.getElementById("status").style.color = "#00ff99";

            } else {

                document.getElementById("status").style.color = "#ff4d4d";

            }

        });

}

setInterval(updateStats, 500);


// ----------------------------
// Capture Button
// ----------------------------

document.getElementById("captureBtn").addEventListener("click", function () {

    fetch("/capture")
        .then(response => response.json())
        .then(data => {

            if (data.success) {

                showNotification("📸 Screenshot Saved");

            } else {

                showNotification("❌ Capture Failed");

            }

        });

});


// ----------------------------
// Notification
// ----------------------------

function showNotification(message) {

    const notification = document.createElement("div");

    notification.className = "notification";

    notification.innerHTML = message;

    document.body.appendChild(notification);

    setTimeout(() => {

        notification.classList.add("show");

    }, 100);

    setTimeout(() => {

        notification.classList.remove("show");

        setTimeout(() => {

            notification.remove();

        }, 300);

    }, 2500);

}


// ----------------------------
// Live Clock
// ----------------------------

setInterval(() => {

    const now = new Date();

    document.title =
        "🤖 AI Sentinel • " +
        now.toLocaleTimeString();

}, 1000);


// ----------------------------
// Button Hover Effect
// ----------------------------

const buttons = document.querySelectorAll("button");

buttons.forEach(btn => {

    btn.addEventListener("mouseenter", () => {

        btn.style.transform = "scale(1.05)";

    });

    btn.addEventListener("mouseleave", () => {

        btn.style.transform = "scale(1)";

    });

});


// Initial Update

updateStats();
```
