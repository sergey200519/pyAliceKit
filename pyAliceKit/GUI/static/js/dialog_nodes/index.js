import { fetchDialogNodes, fetchAllMessages } from "./fetcher.js";
import { drawDialogNodes, drawAllMessages } from "./drawer.js";

document.addEventListener("DOMContentLoaded", () => {
    fetchDialogNodes(drawDialogNodes);
    fetchAllMessages(drawAllMessages);
});

window.addEventListener("resize", () => {
    document.querySelector(".graph_container").innerHTML = "";
    fetchDialogNodes(drawDialogNodes);
});
