// Configuración de los pasos del formulario
const steps = [
    {
        title: "Edad y Sexo",
        questions: [
            { label: "Edad", type: "number", name: "age", placeholder: "Ej: 30", required: true },
            { label: "Sexo", type: "radio", name: "gender", options: ["Femenino", "Masculino"], required: true },
        ],
    },
    {
        title: "Tabaquismo",
        questions: [
            { label: "¿Fuma?", type: "switch", name: "smoking" },
            { label: "¿Tienes dedos amarillos?", type: "switch", name: "yellow_fingers" },
        ],
    },
    // Más pasos según la estructura
];

// Elementos del DOM
const formTitle = document.getElementById("form-title");
const stepIndicator = document.getElementById("step-indicator");
const stepContainer = document.getElementById("step-container");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");

// Estado actual
let currentStep = 0;

// Renderizar el indicador de pasos
steps.forEach((_, index) => {
    const stepBadge = document.createElement("span");
    stepBadge.className = "badge bg-secondary mx-1";
    stepBadge.textContent = index + 1;
    stepBadge.id = `step-indicator-${index}`;
    stepIndicator.appendChild(stepBadge);
});

// Actualizar el contenido del paso
function updateStep() {
    // Título
    formTitle.textContent = steps[currentStep].title;

    // Contenido dinámico
    stepContainer.innerHTML = "";
    steps[currentStep].questions.forEach((question) => {
        const questionDiv = document.createElement("div");
        questionDiv.className = "mb-3";

        const label = document.createElement("label");
        label.textContent = question.label;
        questionDiv.appendChild(label);

        if (question.type === "number") {
            const input = document.createElement("input");
            input.type = "number";
            input.name = question.name;
            input.placeholder = question.placeholder || "";
            input.className = "form-control";
            if (question.required) input.required = true;
            questionDiv.appendChild(input);
        } else if (question.type === "radio") {
            question.options.forEach((option, index) => {
                const radioDiv = document.createElement("div");
                radioDiv.className = "form-check";

                const input = document.createElement("input");
                input.type = "radio";
                input.name = question.name;
                input.value = option;
                input.id = `${question.name}-${index}`;
                input.className = "form-check-input";

                const radioLabel = document.createElement("label");
                radioLabel.textContent = option;
                radioLabel.htmlFor = input.id;
                radioLabel.className = "form-check-label";

                radioDiv.appendChild(input);
                radioDiv.appendChild(radioLabel);
                questionDiv.appendChild(radioDiv);
            });
        } else if (question.type === "switch") {
            const switchDiv = document.createElement("div");
            switchDiv.className = "form-check form-switch";

            const input = document.createElement("input");
            input.type = "checkbox";
            input.name = question.name;
            input.className = "form-check-input";
            switchDiv.appendChild(input);

            questionDiv.appendChild(switchDiv);
        }
        stepContainer.appendChild(questionDiv);
    });

    // Actualizar botones
    prevBtn.disabled = currentStep === 0;
    nextBtn.textContent = currentStep === steps.length - 1 ? "Enviar" : "Siguiente";

    // Actualizar indicador de paso
    steps.forEach((_, index) => {
        const stepBadge = document.getElementById(`step-indicator-${index}`);
        stepBadge.className = `badge mx-1 ${
            index === currentStep ? "bg-primary text-light" : "bg-secondary"
        }`;
    });
}

// Navegación entre pasos
prevBtn.addEventListener("click", () => {
    if (currentStep > 0) {
        currentStep--;
        updateStep();
    }
});

nextBtn.addEventListener("click", () => {
    if (currentStep < steps.length - 1) {
        currentStep++;
        updateStep();
    } else {
        // Enviar formulario
        alert("Formulario enviado!");
    }
});

// Inicializar el primer paso
updateStep();
