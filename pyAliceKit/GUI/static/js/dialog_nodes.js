async function fetchDialogNodes() {
  try {
    const response = await fetch(`${window.location.origin}/api/settings/get_const?key=DIALOG_NODES`);
    if (!response.ok) throw new Error("Ошибка загрузки настроек");
    const data = await response.json();

    if (data.DIALOG_NODES) {
      drawGraph(data.DIALOG_NODES);
    } else {
      throw new Error("Ключ DIALOG_NODES не найден в ответе");
    }
  } catch (error) {
    document.querySelector(".container").innerHTML += `<p class="error-message">Ошибка: ${error.message}</p>`;
  }
}

function parseDialogNodes(dialogNodes) {
  const nodes = [];
  const edges = [];

  function traverse(currentKey, currentValue, parentKey = null, depth = 0) {
    nodes.push({
      id: currentKey,
      label: currentKey,
      meta: currentValue.meta,
      message: currentValue.message,
      depth
    });

    if (parentKey) {
      edges.push({ from: parentKey, to: currentKey });
    }

    if (currentValue.transitions) {
      for (const [, target] of Object.entries(currentValue.transitions)) {
        if (!target.startsWith("$")) {
          edges.push({ from: currentKey, to: target });
        }
      }
    }

    if (currentValue.childs) {
      for (const [childKey, childValue] of Object.entries(currentValue.childs)) {
        traverse(childKey, childValue, currentKey, depth + 1);
      }
    }
  }

  for (const [key, value] of Object.entries(dialogNodes)) {
    traverse(key, value, null, 0);
  }

  return { nodes, edges };
}

function drawGraph(dialogNodes) {
  const { nodes, edges } = parseDialogNodes(dialogNodes);
  const graph = document.getElementById("graph");

  // Очистка и инициализация
  graph.innerHTML = "";
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", "100%");
  svg.setAttribute("height", "2000");
  svg.id = "lines";
  graph.appendChild(svg);

  // Сортировка узлов по глубине
  const depthMap = {};
  nodes.forEach((node) => {
    if (!depthMap[node.depth]) depthMap[node.depth] = [];
    depthMap[node.depth].push(node);
  });

  const layout = {}; // координаты центров для линий

  for (const depth in depthMap) {
    const items = depthMap[depth];
    items.forEach((node, index) => {
      const el = document.createElement('div');
      el.className = 'node';
      el.id = 'node-' + node.id;

      const top = index * 160;
      const left = node.depth * 300;

      layout[node.id] = {
        x: left + 75,
        y: top + 40
      };

      el.style.top = `${top}px`;
      el.style.left = `${left}px`;
      el.innerHTML = `<strong>${node.label}</strong><br><small>${node.meta?.desc || ''}</small>`;
      graph.appendChild(el);
    });
  }

  // Отрисовка связей
  edges.forEach(({ from, to }) => {
    const fromPos = layout[from];
    const toPos = layout[to];
    if (fromPos && toPos) {
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", fromPos.x);
      line.setAttribute("y1", fromPos.y);
      line.setAttribute("x2", toPos.x);
      line.setAttribute("y2", toPos.y);
      line.setAttribute("stroke", "#000");
      line.setAttribute("stroke-width", "2");
      svg.appendChild(line);
    }
  });
}

document.addEventListener("DOMContentLoaded", fetchDialogNodes);
