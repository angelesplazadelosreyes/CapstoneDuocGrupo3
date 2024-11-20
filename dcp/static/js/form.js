// Función para validar y cambiar al siguiente paso
function nextTab(tabId) {
    const currentTab = document.querySelector('.tab-pane.active');
    const nextTab = document.getElementById(tabId);
    
    if (currentTab && nextTab) {
        currentTab.classList.remove('show', 'active');
        nextTab.classList.add('show', 'active');
    }
}

// Función para cambiar al paso anterior
function prevTab(tabId) {
    const currentTab = document.querySelector('.tab-pane.active');
    const prevTab = document.getElementById(tabId);

    if (currentTab && prevTab) {
        currentTab.classList.remove('show', 'active');
        prevTab.classList.add('show', 'active');
    }
}

// Función de inicialización para controlar navegación con "Siguiente" y "Atrás"
document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".tab-pane");
    let currentTabIndex = 0;

    const nextBtn = document.getElementById("next-btn");
    const prevBtn = document.getElementById("prev-btn");

    // Mostrar el tab correspondiente al índice actual
    function showTab(index) {
        tabs.forEach((tab, i) => {
            tab.classList.remove("show", "active");
            if (i === index) {
                tab.classList.add("show", "active");
            }
        });
        updateNavigationButtons();
    }

    // Actualizar la visibilidad de los botones "Siguiente" y "Atrás"
    function updateNavigationButtons() {
        prevBtn.style.display = currentTabIndex > 0 ? "inline-block" : "none";
        nextBtn.textContent = currentTabIndex < tabs.length - 1 ? "Siguiente" : "Enviar";
    }

    // Manejar evento de clic en "Siguiente"
    nextBtn.addEventListener("click", () => {
        if (currentTabIndex < tabs.length - 1) {
            nextTab(`step${currentTabIndex + 2}`); // Cambiar al siguiente tab
            currentTabIndex++;
            showTab(currentTabIndex);
        } else {
            // Enviar formulario al llegar al último paso
            document.getElementById("multi-step-form").submit();
        }
    });

    // Manejar evento de clic en "Atrás"
    prevBtn.addEventListener("click", () => {
        if (currentTabIndex > 0) {
            prevTab(`step${currentTabIndex}`); // Cambiar al tab anterior
            currentTabIndex--;
            showTab(currentTabIndex);
        }
    });

    // Inicializar la vista en el primer tab
    showTab(currentTabIndex);
});
