import { showNodePopup, hideNodePopup } from "./popup.js";
import { isParent } from "./utils.js";

export const generateNodeHTML = (node, path) => {
    const nodeId = path.replace(/\//g, "_").replace(/^_/, "");
    const hasTransitions = Array.isArray(node.transitions);
    const hasPrev = hasTransitions && node.transitions.includes("$prev");

    return `
        <div class="node-card" id="${nodeId}">
            <h3>${path}</h3>
            <p><strong>message:</strong> ${node.message || "—"}</p>
            <p><strong>buttons:</strong> ${(node.buttons || []).join(", ") || "—"}</p>
            <p><strong>previous:</strong> 
                <input type="checkbox" ${hasPrev ? "checked" : ""} ${!hasTransitions ? "disabled" : ""}>
            </p>
            <button onclick="showNodePopup('${nodeId}')">Подробнее</button>
            <div class="node-popup" id="popup_${nodeId}" style="display:none;">
                <div class="popup-content">
                    <h4>Детали узла: ${path}</h4>
                    <pre>${JSON.stringify(node, null, 2)}</pre>
                    <button onclick="hideNodePopup('${nodeId}')">Закрыть</button>
                </div>
            </div>
        </div>
    `;
};

export const createBranch = (node, isGlobal = false) => {
    const branchElement = document.createElement("div");
    branchElement.className = isGlobal ? "branch global_branch" : "branch";
    branchElement.id = node.path.replace(/\//g, "_").replace(/^_/, "");
    return branchElement;
};

export const createNode = (dialogNodesMap, path) => {
    const node = dialogNodesMap[path];
    node.path = path;
    const nodeHTML = generateNodeHTML(node, path);

    if (isParent(dialogNodesMap, path)) {
        const branchElement = createBranch(node);
        branchElement.innerHTML = `
            <div class="branch_header">${nodeHTML}</div>
            <div class="branch_childs"></div>
        `;
        return branchElement;
    } else {
        const tempContainer = document.createElement("div");
        tempContainer.innerHTML = nodeHTML.trim();
        return tempContainer.firstElementChild;
    }
};
