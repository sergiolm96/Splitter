document.addEventListener('DOMContentLoaded', function() {
    const loggedIn = document.body.dataset.loggedIn === 'true';
    
    // Mostrar/ocultar secciones basado en el estado de inicio de sesión
    const welcomeScreen = document.getElementById('welcome-screen');
    const appScreen = document.getElementById('app-screen');

    if (loggedIn) {
        welcomeScreen.style.display = 'none';
        appScreen.style.display = 'block';
    } else {
        welcomeScreen.style.display = 'block';
        appScreen.style.display = 'none';
    }
    
    // Mostrar/ocultar enlaces de navegación basado en el estado de inicio de sesión
    document.getElementById('create-group').style.display = loggedIn ? 'block' : 'none';
    document.getElementById('add-expense').style.display = loggedIn ? 'block' : 'none';
    document.getElementById('transactions').style.display = loggedIn ? 'block' : 'none';
    document.getElementById('login').style.display = loggedIn ? 'none' : 'block';
    document.getElementById('register').style.display = loggedIn ? 'none' : 'block';
    document.getElementById('logout').style.display = loggedIn ? 'block' : 'none';
});
