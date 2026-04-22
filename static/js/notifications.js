(function () {

    function wsURL() {
        const loc = window.location;
        const scheme = (loc.protocol === "https:") ? "wss" : "ws";
        return `${scheme}://${loc.host}/ws/notifications/`;
    }

    const socket = new WebSocket(wsURL());

    socket.onopen = () => {
        console.log("✅ WebSocket Connected");
    };

    socket.onclose = () => {
        console.log("❌ WebSocket Disconnected");
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("🔔 Notification received:", data);

        addToDropdown(data);
        bumpBadge();
        showToast(data);
    };


    // 🔔 Increase unread count on bell
    function bumpBadge() {
        const badge = document.getElementById("notif-badge");
        if (!badge) return;
        let current = parseInt(badge.textContent || "0");
        badge.textContent = current + 1;
        badge.style.display = "inline-block";
    }


    // 🔽 Add notification to dropdown (top of list)
    function addToDropdown(n) {
        const root = document.getElementById("notif-items");
        if (!root) return;

        const li = document.createElement("li");
        li.innerHTML = `
            <a class="dropdown-item fw-semibold" href="${n.url || "#"}" data-id="${n.id}">
                ${n.verb}
                <small class="text-muted d-block">just now</small>
            </a>
        `;
        root.prepend(li);
    }


    // ✅ Toast popup when notification arrives
    function showToast(n) {
        let toast = document.createElement("div");
        toast.className = "notification-toast";
        toast.innerHTML = `
            <div class="toast-body">
                🔔 ${n.verb}
            </div>
        `;

        Object.assign(toast.style, {
            position: "fixed",
            right: "20px",
            bottom: "20px",
            padding: "12px 18px",
            background: "#222",
            color: "#fff",
            borderRadius: "8px",
            zIndex: "9999",
            animation: "fadeOut 4s forwards"
        });

        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }

})();