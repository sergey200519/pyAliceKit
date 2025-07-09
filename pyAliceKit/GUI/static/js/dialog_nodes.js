// ==== Утилиты ====

const getParentNodeId = (path) => {
    const parts = path.split("/");
    if (parts.length <= 1) return null;
    parts.pop();
    return parts.join("/").replace(/\//g, "_").replace(/^_/, "");
};

const isParent = (dialogNodesMap, path) => {
    const node = dialogNodesMap[path];
    return Array.isArray(node?.childs) && node.childs.length > 0;
};

const flattenDialogs = (dialogs) => {
    const result = {};

    function walk(node, path) {
        const { childs, ...flatNode } = node;

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
};

// ==== Генерация HTML ====

const generateNodeHTML = (node, path) => {
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

const createBranch = (node, isGlobal = false) => {
    const branchElement = document.createElement("div");
    branchElement.className = isGlobal ? "branch global_branch" : "branch";
    branchElement.id = node.path.replace(/\//g, "_").replace(/^_/, "");
    return branchElement;
};

const createNode = (dialogNodesMap, path) => {
    const node = dialogNodesMap[path];
    node.path = path;
    const nodeHTML = generateNodeHTML(node, path);

    if (isParent(dialogNodesMap, path)) {
        const branchElement = createBranch(node);
        branchElement.innerHTML = `
            <div class="branch_header">
                ${nodeHTML}
            </div>
            <div class="branch_childs"></div>
        `;
        return branchElement;
    } else {
        const tempContainer = document.createElement("div");
        tempContainer.innerHTML = nodeHTML.trim();
        return tempContainer.firstElementChild;
    }
};

// ==== UI ====

const showNodePopup = (id) => {
    document.getElementById("popup_" + id).style.display = "block";
};

const hideNodePopup = (id) => {
    document.getElementById("popup_" + id).style.display = "none";
};

// ==== Отрисовка ====

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
            } else {
                console.error(`Не найден контейнер дочерних узлов для ${node.path}`);
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

const drawDialogNodes = (dialogNodes) => {
    const dialogNodesMap = flattenDialogs(dialogNodes);
    const graphContainer = document.querySelector(".graph_container");
    let generation = 1;

    while (generation <= 100) {
        const count = drawGenerations(dialogNodesMap, graphContainer, generation);
        if (count === 0) break;
        generation++;
    }
};

// ==== Загрузка ====

const fetchDialogNodes = async () => {
    try {
        const response = await fetch(
            `${window.location.origin}/api/settings/get_const?key=DIALOG_NODES`
        );
        if (!response.ok) throw new Error("Ошибка загрузки настроек");

        const data = await response.json();
        if (data.DIALOG_NODES) {
            drawDialogNodes(data.DIALOG_NODES);
        } else {
            throw new Error("Ключ DIALOG_NODES не найден в ответе");
        }
    } catch (error) {
        document.querySelector(".container").innerHTML += `
            <p class="error-message">Ошибка: ${error.message}</p>
        `;
    }
};

document.addEventListener("DOMContentLoaded", fetchDialogNodes);
