document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginErrorMessage = document.getElementById('loginErrorMessage');
    const loginModal = document.getElementById('loginModal');

    // Evento para limpiar el mensaje de error, los campos y reiniciar el formulario cuando el modal se cierra
    $('#loginModal').on('hidden.bs.modal', function() {
        console.log("Modal cerrado, reiniciando formulario y limpiando mensajes.");
        loginErrorMessage.style.display = 'none';  // Oculta el mensaje de error
        loginErrorMessage.textContent = '';  // Limpia el texto del mensaje de error
        loginForm.reset();  // Reinicia el formulario a su estado inicial
        // Limpieza manual de campos para asegurar que no queden valores residuales
        loginForm.querySelector('[name="username"]').value = '';
        loginForm.querySelector('[name="password"]').value = '';
    });

    // Manejo del envío del formulario mediante AJAX
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Evita el envío normal del formulario

        // Limpia cualquier mensaje de error antes de enviar los datos
        loginErrorMessage.style.display = 'none';
        loginErrorMessage.textContent = '';

        console.log("Enviando datos de inicio de sesión...");

        // Crea una solicitud AJAX para enviar los datos del formulario
        fetch(loginForm.action, {
            method: 'POST',
            body: new FormData(loginForm),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // Identifica la solicitud como AJAX
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta recibida del servidor:", data);

            if (data.success) {
                console.log("Inicio de sesión exitoso, redirigiendo...");
                // Si la autenticación es exitosa, redirige al dashboard
                window.location.href = data.redirect_url;
            } else {
                console.log("Error en las credenciales: mostrando mensaje de error.");
                // Si falla, muestra el mensaje de error en el modal
                loginErrorMessage.style.display = 'block';
                loginErrorMessage.textContent = data.error;

                // Limpia los campos de usuario y contraseña para que el usuario pueda volver a intentarlo
                loginForm.querySelector('[name="username"]').value = '';
                loginForm.querySelector('[name="password"]').value = '';
            }
        })
        .catch(error => {
            console.error("Error de red o de servidor:", error);
            loginErrorMessage.style.display = 'block';
            loginErrorMessage.textContent = 'Ocurrió un error inesperado. Inténtelo de nuevo más tarde.';

            // Limpia los campos de usuario y contraseña en caso de un error inesperado
            loginForm.querySelector('[name="username"]').value = '';
            loginForm.querySelector('[name="password"]').value = '';
        });
    });
});
