export const showNodePopup = (id) => {
    document.getElementById("popup_" + id).style.display = "block";
};

export const hideNodePopup = (id) => {
    document.getElementById("popup_" + id).style.display = "none";
};
