const menu = document.getElementById("menu");
const menu_button = document.getElementById("menu-button");

let isMenuHidden = true;

function toggle_nav_popup() {
    isMenuHidden = !isMenuHidden;
    menu.hidden = isMenuHidden;
}

menu_button.addEventListener("click", function(event) {
    event.stopPropagation();
    toggle_nav_popup();
});

// Закрываем меню при клике в любом месте
document.addEventListener("click", function(event) {
    if (!isMenuHidden) {
        isMenuHidden = true;
        menu.hidden = true;
    }
});