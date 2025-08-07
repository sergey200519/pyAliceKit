export const flattenDialogs = (dialogs) => {
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

export const getParentNodeId = (path) => {
    const parts = path.split("/");
    if (parts.length <= 1) return null;
    parts.pop();
    return parts.join("/").replace(/\//g, "_").replace(/^_/, "");
};

export const isParent = (dialogNodesMap, path) => {
    const node = dialogNodesMap[path];
    return Array.isArray(node?.childs) && node.childs.length > 0;
};
