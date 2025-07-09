const getNodeHTML = (dialogNodesMap, path) => {
    const node = dialogNodesMap[path];
    if (!node) return `<div class="error">Узел "${path}" не найден.</div>`;

    const nodeId = path.replace(/\//g, "_").replace(/^_/, "");
    
    return `
        <div class="node-card" id="${nodeId}">
            <h3>${path}</h3>
            <p><strong>message:</strong> ${node.message || "—"}</p>
            <p><strong>buttons:</strong> ${(node.buttons || []).join(", ") || "—"}</p>
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

const isParent = (dialogNodesMap, path) => {
    const node = dialogNodesMap[path];
    return Array.isArray(node?.childs) && node.childs.length > 0;
};

const createBranch = () => {
    
}

const createNode = (dialogNodes, dialogNodesMap, path, isGlobal) => {
    
}

// TODO: Redesign the modal window system
function showNodePopup(id) {
    document.getElementById("popup_" + id).style.display = "block";
}

function hideNodePopup(id) {
    document.getElementById("popup_" + id).style.display = "none";
}

const getGeneration = (dialogNodesMap, nSlash) =>
    Object.entries(dialogNodesMap)
        .filter(([path, _]) => path.split("/").filter(Boolean).length === nSlash)
        .map(([path, value]) => ({ path, ...value }));

const drawFirstGeneration = (dialogNodes, dialogNodesMap, graphContainer) => {
    const nodes = getGeneration(dialogNodesMap, 1);
    if (nodes.length === 0) return 0;
    nodes.forEach((node) => {
        const nodeElement = document.createElement("div");
        nodeElement.className = "branch global_branch";
        nodeElement.id = node.path.replace(/\//g, "_").replace(/^_/, "");
        nodeElement.innerHTML = `
            <div class="branch_header">
                ${getNodeHTML(dialogNodesMap, node.path)}
            </div>
            <div class="branch_childs">
            </div>
            `;
        graphContainer.appendChild(nodeElement);
    });
};

const drawGenerations = (
    dialogNodes,
    dialogNodesMap,
    graphContainer,
    generation
) => {
    if (generation === 1)
        return drawFirstGeneration(dialogNodes, dialogNodesMap, graphContainer);

    const nodes = getGeneration(dialogNodesMap, generation);
    console.log(`Generation ${generation} nodes:`, nodes);


    return nodes.length
};

const drawDialogNodes = (dialogNodes, dialogNodesMap) => {
    console.log(dialogNodesMap);
    const graphContainer = document.querySelector(".graph_container");
    var i = 1;
    while (true) {
        count = drawGenerations(dialogNodes, dialogNodesMap, graphContainer, i);
        if (count === 0) break;
        i++;
        if (i > 100) break;
    }
};

async function fetchDialogNodes() {
    try {
        const response = await fetch(
            `${window.location.origin}/api/settings/get_const?key=DIALOG_NODES`
        );
        if (!response.ok) throw new Error("Ошибка загрузки настроек");
        const data = await response.json();

        if (data.DIALOG_NODES) {
            drawDialogNodes(data.DIALOG_NODES, flattenDialogs(data.DIALOG_NODES));
        } else {
            throw new Error("Ключ DIALOG_NODES не найден в ответе");
        }
    } catch (error) {
        document.querySelector(
            ".container"
        ).innerHTML += `<p class="error-message">Ошибка: ${error.message}</p>`;
    }
}

function flattenDialogs(dialogs, basePath = "") {
    const result = {};

    function walk(node, path) {
        const { childs, ...flatNode } = node;

        // Если chooser — строка функции, сохранить её и имя
        if (flatNode.chooser && typeof flatNode.chooser === "string") {
            const match = flatNode.chooser.match(/def\s+(\w+)/);
            if (match) {
                flatNode.chooser_name = match[1];
                flatNode.chooser = flatNode.chooser.trim();
            }
        }

        const fullPath = `/${path}`;
        const childPaths = [];

        if (childs && typeof childs === "object") {
            for (const [childKey, childNode] of Object.entries(childs)) {
                const childPath = `${path}/${childKey}`;
                childPaths.push(`/${childPath}`);
                walk(childNode, childPath);
            }
        }

        if (childPaths.length > 0) {
            flatNode.childs = childPaths;
        }

        result[fullPath] = flatNode;
    }

    for (const [key, node] of Object.entries(dialogs)) {
        walk(node, key);
    }

    return result;
}

document.addEventListener("DOMContentLoaded", fetchDialogNodes);
