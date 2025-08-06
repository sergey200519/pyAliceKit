document.addEventListener("DOMContentLoaded", async () => {
    const container = document.querySelector(".buttons");

    // Утилита для создания секций
    function createSection(titleText) {
        const section = document.createElement("section");
        section.classList.add("section");

        const title = document.createElement("h2");
        title.textContent = titleText;
        section.appendChild(title);

        return section;
    }

    try {
        const [buttonsRes, constRes, groupsRes, startingRes, keywordsRes] = await Promise.all([
            fetch(`${window.location.origin}/api/settings/get_const_fresh?key=BUTTONS`),
            fetch(`${window.location.origin}/api/settings/get_const_fresh?key=CONSTANT_BUTTONS`),
            fetch(`${window.location.origin}/api/settings/get_const_fresh?key=BUTTONS_GROUPS`),
            fetch(`${window.location.origin}/api/settings/get_const_fresh?key=STARTING_BUTTONS`),
            fetch(`${window.location.origin}/api/settings/get_const_fresh?key=KEY_WORDS`)
        ]);

        const BUTTONS = (await buttonsRes.json()).BUTTONS;
        const CONSTANT_BUTTONS = (await constRes.json()).CONSTANT_BUTTONS;
        const BUTTONS_GROUPS = (await groupsRes.json()).BUTTONS_GROUPS;
        const STARTING_BUTTONS = (await startingRes.json()).STARTING_BUTTONS;
        const KEY_WORDS = (await keywordsRes.json()).KEY_WORDS;

        // ----- Отрисовка всех BUTTONS -----
        const btnsSection = createSection("Все кнопки");
        const btnsList = document.createElement("ul");

        for (const [key, { title, hide }] of Object.entries(BUTTONS)) {
            const li = document.createElement("li");
            li.innerHTML = `<strong>${key}</strong>: ${title} ${hide ? "<em>(скрыта)</em>" : ""}`;
            btnsList.appendChild(li);
        }

        btnsSection.appendChild(btnsList);
        container.appendChild(btnsSection);

        // ----- CONSTANT_BUTTONS -----
        const constSection = createSection("Константные кнопки");
        const constList = document.createElement("ul");
        CONSTANT_BUTTONS.forEach((btn) => {
            const li = document.createElement("li");
            li.textContent = btn;
            constList.appendChild(li);
        });
        constSection.appendChild(constList);
        container.appendChild(constSection);

        // ----- BUTTONS_GROUPS -----
        const groupsSection = createSection("Группы кнопок");
        for (const [group, buttons] of Object.entries(BUTTONS_GROUPS)) {
            const groupDiv = document.createElement("div");
            groupDiv.classList.add("group");

            const title = document.createElement("h3");
            title.textContent = group;
            groupDiv.appendChild(title);

            const list = document.createElement("ul");
            buttons.forEach((btnKey) => {
                const li = document.createElement("li");
                li.textContent = btnKey + (CONSTANT_BUTTONS.includes(btnKey) ? " ⚠️" : "");
                list.appendChild(li);
            });

            groupDiv.appendChild(list);
            groupsSection.appendChild(groupDiv);
        }
        container.appendChild(groupsSection);

        // ----- STARTING_BUTTONS -----
        const startSection = createSection("Стартовые кнопки");
        if (STARTING_BUTTONS.length === 0) {
            startSection.appendChild(document.createTextNode("Пусто"));
        } else {
            const startList = document.createElement("ul");
            STARTING_BUTTONS.forEach(btn => {
                const li = document.createElement("li");
                li.textContent = btn;
                startList.appendChild(li);
            });
            startSection.appendChild(startList);
        }
        container.appendChild(startSection);

        // ----- KEY_WORDS -----
        const keyWordsSection = createSection("Ключевые слова");
        for (const [key, words] of Object.entries(KEY_WORDS)) {
            const kwDiv = document.createElement("div");
            const label = document.createElement("h3");
            label.textContent = key;
            kwDiv.appendChild(label);

            const list = document.createElement("ul");
            words.forEach(word => {
                const li = document.createElement("li");
                li.textContent = word;
                list.appendChild(li);
            });

            kwDiv.appendChild(list);
            keyWordsSection.appendChild(kwDiv);
        }
        container.appendChild(keyWordsSection);

    } catch (error) {
        console.error("Ошибка загрузки данных:", error);
        container.innerHTML = "<p>Ошибка загрузки данных. Проверьте консоль.</p>";
    }
});
