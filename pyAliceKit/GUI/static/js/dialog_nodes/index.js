import { fetchDialogNodes } from "./fetcher.js";
import { drawDialogNodes } from "./drawer.js";

document.addEventListener("DOMContentLoaded", () => {
    fetchDialogNodes(drawDialogNodes);
});

window.addEventListener("resize", () => {
    document.querySelector(".graph_container").innerHTML = "";
    fetchDialogNodes(drawDialogNodes);
});
