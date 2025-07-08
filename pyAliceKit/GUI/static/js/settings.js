const requiredKeys = [
    "DEBUG",
    "DEBUG_LANGUAGE",
    "LANGUAGE",
    "SOURCE_TEXT",
    "EVENTS",
    "LOG_OUTPUT_IMMEDIATELY",
    "VERSION",
    "TEXT_FOR_KEY_WORDS",
    "KEY_WORDS",
    "DIALOG_NODES",
    "DIALOGS_MAP_FILE",
    "ALL_MESSAGES",
    "STARTING_MESSAGE",
    "ERROR_MESSAGE",
    "HELP_MESSAGE",
    "BUTTONS",
    "BUTTONS_GROUPS",
    "CONSTANT_BUTTONS",
    "STARTING_BUTTONS",
    "IMAGES",
];

const selectKeys = {
    "DEBUG_LANGUAGE": ["ru", "en", "de", "fr", "es", "it", "pt", "zh", "ja"],
    "LANGUAGE": ["ru", "en", "de", "fr", "es", "it", "pt", "zh", "ja"],
    "LANGUAGE": ["ru", "en", "de", "fr", "es", "it", "pt", "zh", "ja"],
    "SOURCE_TEXT": ["command", "original_utterance"],
    "TEXT_FOR_KEY_WORDS": ["command", "original_utterance"],
}

const redirectKeys = {
    "KEY_WORDS": "/key_words.html",
    "DIALOG_NODES": "/dialog_nodes.html",
    "ALL_MESSAGES": "/messages.html",
    "BUTTONS": "/buttons.html",
    "BUTTONS_GROUPS": "/buttons.html",
    "CONSTANT_BUTTONS": "/buttons.html",
    "STARTING_BUTTONS": "/buttons.html",
    "IMAGES": "/images.html",
}

async function fetchSettings() {
    try {
        const response = await fetch(`${window.location.origin}/api/settings/get_all`);
        if (!response.ok) throw new Error("Ошибка загрузки настроек");

        const data = await response.json();
        const container = document.querySelector(".settings_box");

        const requiredSection = document.createElement("div");
        requiredSection.className = "settings-section required-settings";
        requiredSection.innerHTML = `<h3 class="section-title">Обязательные настройки</h3>`;

        const optionalSection = document.createElement("div");
        optionalSection.className = "settings-section optional-settings";
        optionalSection.innerHTML = `<h3 class="section-title">Дополнительные настройки</h3>`;

        const keysSet = new Set(Object.keys(data));

        requiredKeys.forEach(key => {
            if (keysSet.has(key)) {
                const settingElement = createSettingElement(key, data[key]);
                requiredSection.appendChild(settingElement);
                keysSet.delete(key);
            }
        });

        [...keysSet].sort().forEach(key => {
            const settingElement = createSettingElement(key, data[key]);
            optionalSection.appendChild(settingElement);
        });

        container.appendChild(requiredSection);
        container.appendChild(optionalSection);

    } catch (error) {
        document.querySelector(".container").innerHTML += `<p class="error-message">Ошибка: ${error.message}</p>`;
    }
}

function createSettingElement(key, value) {
  const wrapper = document.createElement("div");
  wrapper.className = "setting-item";

  // Название настройки
  const label = document.createElement("label");
  label.textContent = key;
  label.setAttribute("for", key);
  label.className = "setting-label";
  wrapper.appendChild(label);

  // Если это redirect — только ссылка и return
  if (redirectKeys[key]) {
    const link = document.createElement("a");
    link.href = redirectKeys[key];
    link.textContent = "Перейти →";
    link.className = "setting-link";
    link.title = "Редактировать " + key;
    wrapper.appendChild(link);
    return wrapper; // завершить здесь, ничего больше не рендерим
  }

  // Boolean → checkbox
  if (typeof value === "boolean") {
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = value;
    input.id = key;
    input.name = key;
    input.className = "setting-input";

    wrapper.appendChild(input);
    wrapper.appendChild(createSaveButton(key, input, "checkbox"));
  }

  // Select → список значений
  else if (selectKeys[key]) {
    const select = document.createElement("select");
    select.id = key;
    select.name = key;
    select.className = "setting-select";

    selectKeys[key].forEach(optionValue => {
      const option = document.createElement("option");
      option.value = optionValue;
      option.textContent = optionValue;
      if (optionValue === value) option.selected = true;
      select.appendChild(option);
    });

    wrapper.appendChild(select);
    wrapper.appendChild(createSaveButton(key, select, "select"));
  }

  // Text / number → input
  else if (typeof value === "string" || typeof value === "number") {
    const input = document.createElement("input");
    input.type = "text";
    input.value = value;
    input.id = key;
    input.name = key;
    input.className = "setting-input";

    wrapper.appendChild(input);
    wrapper.appendChild(createSaveButton(key, input, "text"));
  }

  // Object → JSON
  else {
    const pre = document.createElement("pre");
    pre.textContent = JSON.stringify(value, null, 2);
    pre.className = "setting-pre";
    wrapper.appendChild(pre);
  }

  return wrapper;
}



function createSaveButton(key, input, type) {
    const button = document.createElement("button");
    button.textContent = "Save";
    button.className = "save-button";

    button.addEventListener("click", async () => {
        let value;

        switch (type) {
            case "checkbox":
                value = input.checked;
                break;
            case "select":
                value = input.value;
                break;
            case "text":
            default:
                value = input.value;
                break;
        }

        console.log(`Save [${key}]:`, value);

        try {
            const response = await fetch(`${window.location.origin}/api/settings/change_simple`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ key, value })
            });

            if (!response.ok) {
                throw new Error("Ошибка при сохранении");
            }

            const result = await response.json();
            console.log("Ответ сервера:", result);

            // Визуальный отклик — например, смена цвета или уведомление
            button.textContent = "✔️ Сохранено";
            setTimeout(() => (button.textContent = "Save"), 1500);
        } catch (error) {
            console.error(error);
            button.textContent = "❌ Ошибка";
            setTimeout(() => (button.textContent = "Save"), 2000);
        }
    });

    return button;
}


document.addEventListener("DOMContentLoaded", fetchSettings);