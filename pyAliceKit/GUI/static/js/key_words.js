document.addEventListener("DOMContentLoaded", async () => {
    const container = document.querySelector(".key_words");

    try {
        const response = await fetch(`${window.location.origin}/api/settings/get_const_fresh?key=KEY_WORDS`);
        const json = await response.json();

        const data = json.KEY_WORDS;
        

        if (data) {
            for (const [key, words] of Object.entries(data)) {
                const section = document.createElement("section");
                section.classList.add("key_word_section");

                const title = document.createElement("h2");
                title.textContent = key;
                section.appendChild(title);

                const list = document.createElement("ul");
                words.forEach(word => {
                    const li = document.createElement("li");
                    li.textContent = word;
                    list.appendChild(li);
                });

                section.appendChild(list);
                container.appendChild(section);
            }
        } else {
            container.textContent = "Невозможно загрузить ключевые слова.";
        }
    } catch (error) {
        console.error("Ошибка при загрузке ключевых слов:", error);
        container.textContent = "Ошибка при загрузке данных.";
    }
});
