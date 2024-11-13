document.addEventListener('DOMContentLoaded', function() {
    // Configura el evento de envío del formulario de restablecimiento de contraseña
    const passwordResetForm = document.getElementById('passwordResetForm');
    if (passwordResetForm) {
        passwordResetForm.onsubmit = function(event) {
            event.preventDefault();
            fetch(this.action, {
                method: 'POST',
                body: new FormData(this),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.success) {
                    // Pop-up con el correo enmascarado para confirmación
                    alert(`Se ha enviado un enlace de recuperación al correo: ${data.email}`);
                    console.log(`Enlace enviado a: ${data.email}`);
                    $('#forgotPasswordModal').modal('hide');  // Cierra el modal
                } else {
                    alert('Error al procesar la solicitud. Verifique el nombre de usuario.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error inesperado. Inténtelo de nuevo más tarde.');
            });
        };
    }

    // Mostrar el modal de inicio de sesión si hay mensajes de error de autenticación
    const loginForm = document.querySelector('#loginModal form');
    if (loginForm) {
        loginForm.querySelector('[name="username"]').value = '';
        loginForm.querySelector('[name="password"]').value = '';
    }
});
