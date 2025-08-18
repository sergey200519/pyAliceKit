export const drawArrow = (fromEl, toEl, graphContainer, type = "child") => {
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