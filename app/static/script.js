document.addEventListener('DOMContentLoaded', () => {
    const showModal = (modalId) => {
        document.getElementById(modalId).setAttribute('open', '');
    };
    const closeModal = (modalId) => {
        document.getElementById(modalId).removeAttribute('open');
    };

    // Mostrar modales al hacer clic en los botones correspondientes
    document.getElementById('login-btn').addEventListener('click', () => showModal('login-modal'));
    document.getElementById('register-btn').addEventListener('click', () => showModal('register-modal'));
    document.getElementById('create-group-btn').addEventListener('click', () => showModal('create-group-modal'));
    document.getElementById('add-expense-btn').addEventListener('click', () => showModal('add-expense-modal'));
    document.getElementById('transactions-btn').addEventListener('click', () => showModal('transactions-modal'));
    document.getElementById('account-btn').addEventListener('click', () => showModal('account-modal'));
    document.getElementById('logout-btn').addEventListener('click', () => {
        // Maneja el cierre de sesión aquí
        document.body.dataset.loggedIn = 'false';
        // Opcional: Redirige a la página principal o realiza otra acción
    });

    // Cerrar modales al hacer clic en el botón de cierre
    document.querySelectorAll('.close-btn').forEach(button => {
        button.addEventListener('click', () => closeModal(button.closest('dialog').id));
    });

    // Manejar formularios de la cuenta y eliminación
    document.getElementById('delete-account-form').addEventListener('submit', (event) => {
        event.preventDefault();
        // Maneja la eliminación de la cuenta aquí
        alert('Cuenta eliminada');
        closeModal('account-modal');
    });

    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        // Ejemplo de cómo mostrar un mensaje flash solo una vez
        flashMessages.innerHTML = '<div class="flash success">Mensaje de éxito</div>'; // Ejemplo de mensaje
        setTimeout(() => {
            flashMessages.innerHTML = '';
        }, 5000); // Oculta el mensaje después de 5 segundos (5000 milisegundos)
    }
});
