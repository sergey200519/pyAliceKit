export const fetchDialogNodes = async (drawDialogNodes) => {
    const response = await fetch(`${window.location.origin}/api/settings/get_dialog_nodes`);
    if (!response.ok) throw new Error("Ошибка загрузки настроек");

    const data = await response.json();
    if (data.flat) {
        drawDialogNodes(data.flat);
    } else if (data.value) {    
        drawDialogNodes(data.value, false);
    } else {
        throw new Error("Ключ flat не найден в ответе");
    }
};
