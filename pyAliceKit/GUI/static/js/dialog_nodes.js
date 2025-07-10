// ==== Утилиты ====

const drawArrow = (fromEl, toEl, graphContainer, type = "child") => {
    if (fromEl.classList.contains("branch")) {
        fromEl = fromEl.querySelector(".node-card");
    }
    if (toEl.classList.contains("branch")) {
        toEl = toEl.querySelector(".node-card");
    }

    const fromRect = fromEl.getBoundingClientRect();
    const toRect = toEl.getBoundingClientRect();
    const containerRect = graphContainer.getBoundingClientRect();

    // Вычисляем возможные точки начала и конца для каждого направления
    const points = {
        right: {
            x1: fromRect.right - containerRect.left,
            y1: fromRect.top + fromRect.height / 2 - containerRect.top,
            x2: toRect.left - containerRect.left,
            y2: toRect.top + toRect.height / 2 - containerRect.top,
        },
        left: {
            x1: fromRect.left - containerRect.left,
            y1: fromRect.top + fromRect.height / 2 - containerRect.top,
            x2: toRect.right - containerRect.left,
            y2: toRect.top + toRect.height / 2 - containerRect.top,
        },
        down: {
            x1: fromRect.left + fromRect.width / 2 - containerRect.left,
            y1: fromRect.bottom - containerRect.top,
            x2: toRect.left + toRect.width / 2 - containerRect.left,
            y2: toRect.top - containerRect.top,
        },
        up: {
            x1: fromRect.left + fromRect.width / 2 - containerRect.left,
            y1: fromRect.top - containerRect.top,
            x2: toRect.left + toRect.width / 2 - containerRect.left,
            y2: toRect.bottom - containerRect.top,
        }
    };

    // Функция для расчёта длины между двумя точками
    const distance = (p1, p2) => {
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        return Math.sqrt(dx * dx + dy * dy);
    };

    // Вычисляем длины стрелок для всех направлений
    const distances = {};
    for (const dir in points) {
        const p = points[dir];
        distances[dir] = distance({ x: p.x1, y: p.y1 }, { x: p.x2, y: p.y2 });
    }

    // Выбираем направление с минимальной длиной
    let minDir = "right";
    let minDist = distances["right"];
    for (const dir in distances) {
        if (distances[dir] < minDist) {
            minDir = dir;
            minDist = distances[dir];
        }
    }

    // Используем точки выбранного направления
    const { x1, y1, x2, y2 } = points[minDir];

    const dx = x2 - x1;
    const dy = y2 - y1;
    const length = Math.sqrt(dx * dx + dy * dy);
    const angle = Math.atan2(dy, dx) * 180 / Math.PI;

    const arrow = document.createElement("div");
    arrow.className = `arrow ${type}`;
    arrow.style.position = "absolute";
    arrow.style.left = `${x1}px`;
    arrow.style.top = `${y1}px`;
    arrow.style.width = `${length}px`;
    arrow.style.height = "2px";
    arrow.style.transform = `rotate(${angle}deg)`;
    arrow.style.transformOrigin = "left center";

    graphContainer.appendChild(arrow);
};


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
    console.log(node);

    // Проверяем наличие transitions и наличие "$prev" в transitions
    const hasTransitions = Array.isArray(node.transitions);
    const hasPrev = hasTransitions && node.transitions.includes("$prev");

    return `
        <div class="node-card" id="${nodeId}">
            <h3>${path}</h3>
            <p><strong>message:</strong> ${node.message || "—"}</p>
            <p><strong>buttons:</strong> ${(node.buttons || []).join(", ") || "—"}</p>
            <p><strong>previous:</strong> 
                <input type="checkbox" 
                    ${hasPrev ? "checked" : ""} 
                    ${!hasTransitions ? "disabled" : ""}
                >
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
    console.log(nodes);
    
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
    console.log(dialogNodesMap);
    
    const graphContainer = document.querySelector(".graph_container");

    var generation = 1;

    while (generation <= 100) {
        const count = drawGenerations(dialogNodesMap, graphContainer, generation);
        if (count === 0) break;
        generation++;
    }

    // После отрисовки — рисуем стрелки
    for (const [path, node] of Object.entries(dialogNodesMap)) {
        const parentEl = document.getElementById(path.replace(/\//g, "_").replace(/^_/, ""));
        if (!parentEl) continue;

        // Основные связи по childs
        if (Array.isArray(node.childs)) {
            node.childs.forEach((childPath) => {
                const childEl = document.getElementById(childPath.replace(/\//g, "_").replace(/^_/, ""));
                drawArrow(parentEl, childEl, graphContainer);
            });
        }

        // Дополнительные переходы
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

// ==== Загрузка ====

const fetchDialogNodes = async () => {
    // try {
        const response = await fetch(
            `${window.location.origin}/api/settings/get_const_fresh?key=DIALOG_NODES`
        );
        if (!response.ok) throw new Error("Ошибка загрузки настроек");

        const data = await response.json();
        if (data.DIALOG_NODES) {
            drawDialogNodes(data.DIALOG_NODES);
        } else {
            throw new Error("Ключ DIALOG_NODES не найден в ответе");
        }
    // } catch (error) {
    //     document.querySelector(".container").innerHTML += `
    //         <p class="error-message">Ошибка: ${error.message}</p>
    //     `;
    // }
};

document.addEventListener("DOMContentLoaded", fetchDialogNodes);

window.addEventListener("resize", () => {
    document.querySelector(".graph_container").innerHTML = "";
    fetchDialogNodes(); // перерисует всё заново
});
