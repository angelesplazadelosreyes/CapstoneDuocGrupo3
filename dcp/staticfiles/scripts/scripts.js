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
                if (data.success) {
                    alert(`Se ha enviado un enlace de recuperación al correo: ${data.email}`);
                    $('#forgotPasswordModal').modal('hide');
                } else {
                    alert('Error al procesar la solicitud. Verifique el nombre de usuario.');
                }
            })
            .catch(error => console.error('Error:', error));
        };
    }

    // Mostrar el modal si hay mensajes de error de inicio de sesión
    if (document.querySelectorAll('.alert-danger').length > 0) {
        $('#loginModal').modal('show');
    }

    // Limpiar campos de usuario y contraseña si hay un mensaje de error
    const loginForm = document.querySelector('#loginModal form');
    if (loginForm) {
        loginForm.querySelector('[name="username"]').value = '';
        loginForm.querySelector('[name="password"]').value = '';
    }

    // Mostrar pop-up con el mensaje de error si existe
    const messagePopup = document.getElementById('message-popup');
    if (messagePopup && messagePopup.textContent.trim() !== "") {
        alert(messagePopup.textContent.trim());
        $('#loginModal').modal('show');
    }
});
