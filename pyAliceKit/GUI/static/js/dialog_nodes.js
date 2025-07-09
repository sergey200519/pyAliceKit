const getNodeHTML = (dialogNodesMap, path) => {
    const node = dialogNodesMap[path];
    if (!node) return `<div class="error">Узел "${path}" не найден.</div>`;

    const nodeId = path.replace(/\//g, "_").replace(/^_/, "");

    return `
        <div class="node-card" id="${nodeId}">
            <h3>${path}</h3>
            <p><strong>message:</strong> ${node.message || "—"}</p>
            <p><strong>buttons:</strong> ${(node.buttons || []).join(", ") || "—"
        }</p>
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

const getParentNodeId = (path) => {
    const parts = path.split("/");
    if (parts.length <= 1) return null; // Нет родителя
    parts.pop(); // Удаляем последний элемент (текущий узел)
    return parts.join("/").replace(/\//g, "_").replace(/^_/, "");
};

const isParent = (dialogNodesMap, path) => {
    const node = dialogNodesMap[path];
    return Array.isArray(node?.childs) && node.childs.length > 0;
};

const createBranch = (node, isGlobal) => {
    console.log(`Создание ветки для узла: ${node.path}`);
    const branchElement = document.createElement("div");
    if (isGlobal) {
        branchElement.className = "branch global_branch";
    } else {
        branchElement.className = "branch";
    }
    branchElement.id = node.path.replace(/\//g, "_").replace(/^_/, "");
    return branchElement;
};

const createNode = (dialogNodes, dialogNodesMap, path) => {
    console.log(`Функция для создание узла для пути: ${path}`);
    const isParentNode = isParent(dialogNodesMap, path);
    const nodeId = path.replace(/\//g, "_").replace(/^_/, "");
    const node = dialogNodesMap[path];
    node.path = path; // Добавляем путь к узлу для дальнейшего использования

    const nodeElementString = `
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
    if (isParentNode) {
        const branchElement = createBranch(node, false);
        branchElement.innerHTML = `
            <div class="branch_header">
                ${nodeElementString}
            </div>
            <div class="branch_childs">
            </div>
        `;
        return branchElement;
    } else {
        const tempContainer = document.createElement("div");
        tempContainer.innerHTML = nodeElementString.trim();
        const nodeElement = tempContainer.firstElementChild;
        return nodeElement;
    }
};

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
    return nodes.length;
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
    console.log(`Построение узлов на уровне ${generation}`, nodes);
    nodes.forEach((node) => {
        console.log(`Создание узла для пути: ${node.path}`);
        const nodeElement = createNode(dialogNodes, dialogNodesMap, node.path);
        // console.log(getParentNodeId(node.path), "iddddddddddddddd", node.path);
        const parentId = getParentNodeId(node.path);
        if (parentId) {
            const parentElement = document.getElementById(parentId);
            if (parentElement) {
                const childsContainer = parentElement.querySelector(".branch_childs");
                if (childsContainer) {
                    console.log(
                        childsContainer,
                        "childsContainer",
                        nodeElement,
                        "nodeElement"
                    );

                    childsContainer.appendChild(nodeElement);
                } else {
                    console.error(
                        `Не найден контейнер для дочерних узлов в родителе: ${parentId}`
                    );
                }
            } else {
                console.error(`Родительский узел с ID ${parentId} не найден.`);
            }
        } else {
            console.error(
                `Не удалось получить ID родительского узла для пути: ${node.path}`
            );
        }
    });

    return nodes.length;
};

const drawDialogNodes = (dialogNodes, dialogNodesMap) => {
    console.log(dialogNodesMap);
    const graphContainer = document.querySelector(".graph_container");
    var i = 1;
    while (true) {
        count = drawGenerations(dialogNodes, dialogNodesMap, graphContainer, i);
        console.log(`Построено ${count} узлов на уровне ${i}`, count === 0);
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
