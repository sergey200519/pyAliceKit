import { createNode, createBranch, generateNodeHTML } from "./node_factory.js";
import { drawArrow } from "./arrows.js";
import { getParentNodeId, flattenDialogs, isParent } from "./utils.js";

const getGeneration = (dialogNodesMap, nSlash) =>
    Object.entries(dialogNodesMap)
        .filter(([path]) => path.split("/").filter(Boolean).length === nSlash)
        .map(([path, value]) => ({ path, ...value }));

const drawGenerations = (dialogNodesMap, graphContainer, generation) => {
    const nodes = getGeneration(dialogNodesMap, generation);
    if (nodes.length === 0) return 0;

    nodes.forEach((node) => {
        const nodeElement = createNode(dialogNodesMap, node.path);
        const parentId = getParentNodeId(node.path);

        if (parentId) {
            const parentElement = document.getElementById(parentId);
            const childsContainer = parentElement?.querySelector(".branch_childs");
            if (childsContainer) {
                childsContainer.appendChild(nodeElement);
            }
        } else {
            const topBranch = createBranch(node, true);
            topBranch.innerHTML = `
                <div class="branch_header">
                    ${generateNodeHTML(node, node.path)}
                </div>
                <div class="branch_childs"></div>
            `;
            graphContainer.appendChild(topBranch);
        }
    });

    return nodes.length;
};

export const drawDialogNodes = (dialogNodes, isFlat = true) => {
    const graphContainer = document.querySelector(".graph_container");
    graphContainer.innerHTML = "";

    const dialogNodesMap = isFlat ? dialogNodes : flattenDialogs(dialogNodes);
    let generation = 1;

    while (generation <= 100) {
        const count = drawGenerations(dialogNodesMap, graphContainer, generation);
        if (count === 0) break;
        generation++;
    }

    for (const [path, node] of Object.entries(dialogNodesMap)) {
        const parentEl = document.getElementById(path.replace(/\//g, "_").replace(/^_/, ""));
        if (!parentEl) continue;

        if (Array.isArray(node.childs)) {
            node.childs.forEach((childPath) => {
                const childEl = document.getElementById(childPath.replace(/\//g, "_").replace(/^_/, ""));
                drawArrow(parentEl, childEl, graphContainer);
            });
        }

        const transitions = Array.isArray(node.transitions)
            ? node.transitions
            : typeof node.transitions === "object"
                ? Object.values(node.transitions)
                : [];

        transitions.forEach((targetPath) => {
            if (!targetPath.startsWith("/")) return;
            const targetEl = document.getElementById(targetPath.replace(/\//g, "_").replace(/^_/, ""));
            drawArrow(parentEl, targetEl, graphContainer, "transition");
        });
    }
};


export const drawAllMessages = (messages) => {
    const container = document.querySelector('.dialogs_messages');
    if (!container) return;

    container.innerHTML = ''; // Очистить перед отрисовкой
    

    for (const [key, value] of Object.entries(messages)) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';

        const keyElement = document.createElement('strong');
        keyElement.textContent = key + ': ';

        const valueElement = document.createElement('span');
        if (typeof value === 'string') {
            valueElement.textContent = value;
        } else {
            valueElement.textContent = JSON.stringify(value, null, 2);
        }

        messageDiv.appendChild(keyElement);
        messageDiv.appendChild(valueElement);
        container.appendChild(messageDiv);
    }
};
