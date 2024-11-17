function nextTab(tabId) {
    const currentTab = document.querySelector('.tab-pane.active'); // Tab activo actual
    const inputs = currentTab.querySelectorAll('input, select, textarea'); // Todos los inputs
    let isValid = true;

    // Validar campos
    inputs.forEach(input => {
        if (input.type === 'number') {
            // Validar rango explícitamente
            const value = input.value; // No convertir aún para manejar vacío
            const min = parseInt(input.getAttribute('min'), 10);
            const max = parseInt(input.getAttribute('max'), 10);

            if (value === "") {
                alert(`El campo edad no puede estar vacío.`);
                input.focus();
                isValid = false;
            } else if (parseInt(value, 10) < min || parseInt(value, 10) > max) {
                alert(`El valor de edad debe estar entre ${min} y ${max}.`);
                input.focus();
                isValid = false;
            }
        } else if (!input.checkValidity()) {
            input.reportValidity(); // Mostrar mensaje nativo del navegador
            isValid = false;
        }
    });

    // Validar botones de radio manualmente
    const genderInputs = currentTab.querySelectorAll('input[name="GENDER"]');
    if (genderInputs.length > 0) {
        const isChecked = Array.from(genderInputs).some(input => input.checked);
        if (!isChecked) {
            alert("Por favor selecciona tu género.");
            isValid = false;
        }
    }

    // Cambiar al siguiente módulo si todo es válido
    if (isValid) {
        const nextTab = new bootstrap.Tab(document.getElementById(tabId));
        nextTab.show();
    }
}
