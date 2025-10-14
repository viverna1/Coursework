const body = document.body;

function createInputPopup(button_id) {
    var bg = document.createElement("div");
    bg.style = `
        position: fixed;
        background-color: #00000035;
        height: 100vh;
        width: 100%;
        top: 0;
        left: 0;
        z-index: 1000;
    `;

    var popup = document.createElement("div");
    popup.style = `
        position: fixed;
        background-color: #E0FBFC;
        height: 200px;
        width: 350px;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        margin: auto;
        border-radius: 10px;
        z-index: 1001;
        padding: 20px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    `;

    var content_list = button_dict[button_id];

    // Создаем форму
    var form = document.createElement("form");
    form.method = "post";
    form.action = content_list[1];
    form.style = `
        display: flex;
        flex-direction: column;
        height: 100%;
    `;

    // Заголовок
    var title = document.createElement("h2");
    title.textContent = content_list[0];
    title.style.margin = "0 0 20px 0";

    // Крестик для закрытия
    var closeBtn = document.createElement("button");
    closeBtn.innerHTML = "×";
    closeBtn.type = "button";
    closeBtn.style = `
        position: absolute;
        top: 10px;
        right: 15px;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
    `;
    closeBtn.onclick = function() {
        body.removeChild(bg);
        body.removeChild(popup);
    };

    // Поле ввода
    var input = document.createElement("input");
    input.type = "text";
    input.name = "value"; // имя для отправки на сервер
    input.className = "inp";
    input.style.marginBottom = "20px";

    // Кнопка submit
    var submitBtnContainer = document.createElement("div");
    submitBtnContainer.className = "button-container";

    var submitBtn = document.createElement("button");
    submitBtn.type = "submit";
    submitBtn.textContent = "Подтвердить";
    submitBtn.className = "btn";

    // Собираем форму
    form.appendChild(title);
    form.appendChild(input);
    form.appendChild(submitBtnContainer);
    submitBtnContainer.appendChild(submitBtn)

    popup.appendChild(closeBtn);
    popup.appendChild(form);

    body.appendChild(bg);
    body.appendChild(popup);

    // Закрытие при клике на фон
    bg.onclick = function() {
        body.removeChild(bg);
        body.removeChild(popup);
    };

    // Фокус на поле ввода
    input.focus();
}

const button_dict = {
    "change-username": ["Введите новое имя:", "/changeUsername"],
    "change-photo": ["Вставьте новое фото:", "/changePhoto"],
    "change-email": ["Введите новую почту:", "/changeEmail"],
    "change-number": ["Введите новый номер:", "/changeNumber"]
}


// Получить кнопки
const buttons = document.querySelectorAll(".settings-button")

// 
buttons.forEach(button => {
    var current_id = button.id;
    console.log(current_id);
    button.addEventListener("click", () => {
        createInputPopup(current_id);
    });
});
