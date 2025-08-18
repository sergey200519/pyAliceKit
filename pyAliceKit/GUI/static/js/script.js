console.log("hi");
const evtSource = new EventSource("/api/updates/events");
let lastServerId = null;

evtSource.onmessage = function(event) {
    const match = event.data.match(/server_id:([^\s]+)/);
    if (match) {
        const serverId = match[1];
        if (lastServerId === null) {
            lastServerId = serverId;
        } else if (serverId !== lastServerId) {
            localStorage.setItem("scrollX", window.scrollX);
            localStorage.setItem("scrollY", window.scrollY);
            window.location.reload();
        }
    }

    if (event.data.startsWith("reload")) {
        localStorage.setItem("scrollX", window.scrollX);
        localStorage.setItem("scrollY", window.scrollY);
        window.location.reload();
    }
};

// Восстановление позиции скролла после загрузки
window.addEventListener("load", () => {
    setTimeout(() => {
        const scrollX = parseInt(localStorage.getItem("scrollX") || "0", 10);
        const scrollY = parseInt(localStorage.getItem("scrollY") || "0", 10);
        window.scrollTo(scrollX, scrollY);
        localStorage.removeItem("scrollX");
        localStorage.removeItem("scrollY");
    }, 1000);
});
