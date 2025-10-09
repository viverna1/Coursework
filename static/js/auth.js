// Функция проверки пароля
function validatePasswords() {
    const password = document.querySelector('input[name="password"]').value;
    const password2 = document.querySelector('input[name="password2"]').value;
    const errorElement = document.getElementById('password-error');
    
    if (password !== password2) {
        errorElement.textContent = 'Пароли не совпадают';
        errorElement.style.display = 'block';
        return false;
    } else {
        errorElement.style.display = 'none';
        return true;
    }
}

// Отправка формы
document.getElementById('register-form').addEventListener('submit', function(e) {
    if (!validatePasswords()) {
        e.preventDefault();  // Прекращение отправки
    }
});