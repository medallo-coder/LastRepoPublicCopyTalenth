

const navbar = document.querySelector('.navbar');

let isDragging = false;
let startX;
let scrollLeft;

navbar.addEventListener('mousedown', (e) => {
    isDragging = true;
    navbar.classList.add('dragging');
    startX = e.pageX - navbar.offsetLeft;
    scrollLeft = navbar.scrollLeft;
});

navbar.addEventListener('mouseleave', () => {
    isDragging = false;
    navbar.classList.remove('dragging');
});

navbar.addEventListener('mouseup', () => {
    isDragging = false;
    navbar.classList.remove('dragging');
});

navbar.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - navbar.offsetLeft;
    const walk = (x - startX) * 2; // Ajusta la velocidad del desplazamiento
    navbar.scrollLeft = scrollLeft - walk;
});

// Soporte para dispositivos táctiles
navbar.addEventListener('touchstart', (e) => {
    startX = e.touches[0].pageX - navbar.offsetLeft;
    scrollLeft = navbar.scrollLeft;
});

navbar.addEventListener('touchmove', (e) => {
    const x = e.touches[0].pageX - navbar.offsetLeft;
    const walk = (x - startX) * 2;
    navbar.scrollLeft = scrollLeft - walk;
});

//Javascrip de edicion de la informacion de nombre , telefono y correo

document.addEventListener("DOMContentLoaded", function () {
    //Id de el formulario para ingresar la informacion 
    const editIcon = document.getElementById("editIconoForm");
    const modal = document.getElementById("InicioModal");
    const closeModal = document.getElementById("closeInicioModal");
    const saveButton = document.getElementById("saveInicio");
    const deleteButton = document.getElementById("deleteInicio");

    // Campos del formulario
    const NombreInput = document.getElementById("Nombre");
    const CorreoInput = document.getElementById("Correo");
    const NumeroInput = document.getElementById("Numero");

    // Elementos donde se mostrará la información guardada
    const displayNombre = document.getElementById("displayNombre");
    const displayCorreo = document.getElementById("displayCorreo");
    const displayNumero = document.getElementById("displayNumero");

    // Función para validar el formato del correo
    function validarCorreo(correo) {
        const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regexCorreo.test(correo);
    }

    // Función para validar que el número de teléfono solo tenga dígitos
    function validarNumero(numero) {
        const regexNumero = /^[0-9]+$/;
        return regexNumero.test(numero);
    }

    // Función para cargar datos guardados
    function loadSavedData() {
        const savedNombre = localStorage.getItem("Nombre") || "";
        const savedCorreo = localStorage.getItem("Correo") || "";
        const savedNumero = localStorage.getItem("Numero") || "";

        // Mostrar datos en el formulario
        NombreInput.value = savedNombre;
        CorreoInput.value = savedCorreo;
        NumeroInput.value = savedNumero;

        // Mostrar datos en pantalla
        displayNombre.textContent = savedNombre || "Sin información";
        displayCorreo.textContent = savedCorreo || "Sin información";
        displayNumero.textContent = savedNumero || "Sin información";
    }

    // Cargar datos almacenados al inicio
    loadSavedData();

    // Abrir modal
    editIcon.addEventListener("click", function () {
        modal.style.display = "block";
    });

    // Cerrar modal
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Guardar datos con validación
    saveButton.addEventListener("click", function (event) {
        event.preventDefault();

        const newNombre = NombreInput.value.trim();
        const newCorreo = CorreoInput.value.trim();
        const newNumero = NumeroInput.value.trim();

        console.log("Intentando guardar...");
        console.log("Nombre:", newNombre);
        console.log("Correo:", newCorreo);
        console.log("Número:", newNumero);

        // Validar campos
        if (!newNombre || !newCorreo || !newNumero) {
            alert("Por favor, completa todos los campos.");
            return;
        }

        if (!validarCorreo(newCorreo)) {
            alert("Por favor, ingresa un correo válido.");
            return;
        }

        if (!validarNumero(newNumero)) {
            alert("Por favor, ingresa un número de teléfono válido.");
            return;
        }

        // Guardar en localStorage
        localStorage.setItem("Nombre", newNombre);
        localStorage.setItem("Correo", newCorreo);
        localStorage.setItem("Numero", newNumero);

        // Actualizar la visualización de los datos
        displayNombre.textContent = newNombre;
        displayCorreo.textContent = newCorreo;
        displayNumero.textContent = newNumero;

        alert("Datos guardados correctamente.");
        modal.style.display = "none"; // Cerrar modal
    });

    // Eliminar información
    deleteButton.addEventListener("click", function () {
        localStorage.removeItem("Nombre");
        localStorage.removeItem("Correo");
        localStorage.removeItem("Numero");

        NombreInput.value = "";
        CorreoInput.value = "";
        NumeroInput.value = "";

        displayNombre.textContent = "Sin información";
        displayCorreo.textContent = "Sin información";
        displayNumero.textContent = "Sin información";

        alert("Datos eliminados.");
        modal.style.display = "none";
    });

    // Cerrar modal si se hace clic fuera de él
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});



//Javascrip de descripcion
document.addEventListener("DOMContentLoaded", function () {
    //Id tomados de los campos del formulario en html de descripcion
    const editIcon = document.getElementById("editDescriptionIcon");
    const modal = document.getElementById("descriptionModal");
    const closeModal = document.getElementById("closeModal");
    const saveButton = document.getElementById("saveDescription");
    const deleteButton = document.getElementById("deleteDescription");
    const descriptionText = document.getElementById("displayDescription");
    const descriptionInput = document.getElementById("descriptionInput");

    // Al hacer clic en el icono de editar, abrir modal con el campo vacío
    editIcon.addEventListener("click", function () {
        modal.style.display = "block";
        descriptionInput.value = ""; // Mostrar vacío
    });

    // Cerrar el modal
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Guardar la nueva descripción
    saveButton.addEventListener("click", function () {
        const newDescription = descriptionInput.value.trim();
        if (newDescription !== "") {
            descriptionText.textContent = newDescription; // Actualiza la descripción
        }
        modal.style.display = "none"; // Cierra el modal
    });

    // Eliminar la descripción (dejar en blanco)
    deleteButton.addEventListener("click", function () {
        descriptionText.textContent = "";
        modal.style.display = "none";
    });

    // Cerrar modal si se hace clic fuera de él
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

//Javascrip de experiencia 
document.addEventListener("DOMContentLoaded", function () {
    // selecciona elementos clave
    const modal = document.getElementById("experienceModal");
    const closeModal = document.getElementById("closeExperienceModal");
    const saveButton = document.getElementById("saveExperience");
    const deleteButton = document.getElementById("deleteExperience"); 
    const experienceContainer = document.getElementById("experienceList");
    const addExperience = document.getElementById("addExperience");
    const editIcon = document.getElementById("openExperienceForm");

    // Campos del formulario
    const jobTitleInput = document.getElementById("jobTitle");
    const companyNameInput = document.getElementById("companyName");
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");

    let experiences = JSON.parse(localStorage.getItem("experiences")) || [];
    let editingIndex = null;
    // carga y muestra la informacion
    function loadExperiences() {
        experienceContainer.innerHTML = ""; // Limpiar antes de cargar
    
        experiences.forEach((exp, index) => {
            const div = document.createElement("div");
            div.classList.add("experience-item");
            div.setAttribute("data-index", index);
            div.style.display = "flex"; 
            div.style.alignItems = "center"; 
            div.style.justifyContent = "space-between"; 
            div.style.padding = "8px"; 
            
    
            // 📌 Contenedor del texto de la experiencia
            const textContainer = document.createElement("div");
            textContainer.innerHTML = `
                <strong>${exp.jobTitle}</strong><br>
                <p>${exp.companyName}</p>
                <p>${exp.startDate} - ${exp.endDate}</p>
            `;
    
            // 📌 Contenedor para mantener la alineación a la derecha
            const actionContainer = document.createElement("div");
    
            // 📌 Si NO es la primera experiencia, añadir el lápiz de edición
            if (index > 0) {
                const editIcon = document.createElement("img");
                editIcon.src = "img/pencil.svg";
                editIcon.alt = "Editar";
                editIcon.style.cursor = "pointer";
                editIcon.style.width = "22px";
    
                // Asegurar que el lápiz esté alineado a la derecha
                actionContainer.style.display = "flex";
                actionContainer.style.alignItems = "center";
                actionContainer.appendChild(editIcon);
    
                // 📌 Evento para abrir modal en modo edición SOLO para esta experiencia
                editIcon.addEventListener("click", function (event) {
                    event.stopPropagation();
                    editingIndex = index;
                    openEditModal(experiences[editingIndex]);
                });
            }
            div.appendChild(textContainer);
            div.appendChild(actionContainer); // Asegura que el lápiz quede a la derecha
            experienceContainer.appendChild(div);
        });
    }
    
    
    
    

    // Abrir modal con datos para editar
    function openEditModal(exp) {
        jobTitleInput.value = exp.jobTitle;
        companyNameInput.value = exp.companyName;
        startDateInput.value = exp.startDate;
        endDateInput.value = exp.endDate;
        deleteButton.style.display = "block";
        modal.style.display = "block";
    }

    // 📌 **Lápiz abre el formulario para editar la primera experiencia**
    editIcon.addEventListener("click", function () {
        if (experiences.length > 0) {
            editingIndex = 0;
            openEditModal(experiences[0]);
        } else {
            alert("No hay experiencias para editar.");
        }
    });

    // Abrir modal vacío para añadir nueva experiencia
    addExperience.addEventListener("click", function () {
        editingIndex = null;
        jobTitleInput.value = "";
        companyNameInput.value = "";
        startDateInput.value = "";
        endDateInput.value = "";
        deleteButton.style.display = "none";
        modal.style.display = "block";
    });

    // Guardar experiencia (nueva o editada)
    saveButton.addEventListener("click", function () {
        const newJobTitle = jobTitleInput.value.trim();
        const newCompanyName = companyNameInput.value.trim();
        const newStartDate = startDateInput.value.trim();
        const newEndDate = endDateInput.value.trim();

        if (newJobTitle && newCompanyName && newStartDate && newEndDate) {
            const newExperience = {
                jobTitle: newJobTitle,
                companyName: newCompanyName,
                startDate: newStartDate,
                endDate: newEndDate
            };

            if (editingIndex !== null) {
                experiences[editingIndex] = newExperience;
            } else {
                experiences.push(newExperience);
            }

            localStorage.setItem("experiences", JSON.stringify(experiences));
            loadExperiences();
            modal.style.display = "none";
        } else {
            alert("Por favor, completa todos los campos.");
        }
    });

    // Eliminar experiencia
    deleteButton.addEventListener("click", function () {
        if (editingIndex !== null && confirm("¿Seguro que quieres eliminar esta experiencia?")) {
            experiences.splice(editingIndex, 1);
            localStorage.setItem("experiences", JSON.stringify(experiences));
            loadExperiences();
            modal.style.display = "none";
        }
    });

    // Cerrar modal
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Cerrar modal si se hace clic fuera
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // Cargar experiencias al iniciar
    loadExperiences();
});

//Javascrip de estudios
document.addEventListener("DOMContentLoaded", function () {
    //Seleciona los elementos clave
    const modal = document.getElementById("estudiosModal");
    const closeModal = document.getElementById("closeEstudiosModal");
    const editButton = document.getElementById("EstudiosForm"); // Botón de edición general (arriba a la derecha)
    const addButton = document.getElementById("addStudies");
    const saveButton = document.getElementById("saveEstudios");
    const deleteButton = document.getElementById("deleteEstudios");
    const studiesList = document.getElementById("studiesList");
    //Campos del formulario

    const titleInput = document.getElementById("TituloObtenido");
    const centerInput = document.getElementById("CentroEducativo");
    const levelInput = document.getElementById("NivelEstudio");
    const startInput = document.getElementById("InicioFecha");
    const endInput = document.getElementById("FinalFecha");

    // se utilizan para mostrar dinámicamente la información
    const displayTitulo = document.getElementById("displayTituloObtenido");
    const displayCentro = document.getElementById("displayCentroEducativo");
    const displayNivel = document.getElementById("displayNivelEstudio");
    const displayInicio = document.getElementById("displayInicioFecha");
    const displayFinal = document.getElementById("displayFinalFecha");

    let editingIndex = null;

    //Abre el modal para ingresar los datos
    function openModal(isEditing, index = null) {
        modal.style.display = "block";
        editingIndex = index;

        if (isEditing && index !== null) {
            const studies = JSON.parse(localStorage.getItem("studies")) || [];
            if (studies[index]) {
                titleInput.value = studies[index].titulo || "";
                centerInput.value = studies[index].centro || "";
                levelInput.value = studies[index].nivel || "";
                startInput.value = studies[index].inicio || "";
                endInput.value = studies[index].final || "";

                deleteButton.style.display = "block";
        // Oculta eliminar en el primer estudio
            }
        } else {
            titleInput.value = "";
            centerInput.value = "";
            levelInput.value = "";
            startInput.value = "";
            endInput.value = "";
            deleteButton.style.display = "none";
        }
    }
    //Para cerrar el modal
    function closeModalFunc() {
        modal.style.display = "none";
        editingIndex = null;
    }
    //Guardar un estudio
    function saveStudy() {
        const studies = JSON.parse(localStorage.getItem("studies")) || [];
        const studyData = {
            titulo: titleInput.value.trim(),
            centro: centerInput.value.trim(),
            nivel: levelInput.value.trim(),
            inicio: startInput.value.trim(),
            final: endInput.value.trim()
        };
            // Verifica que todos los campos estén llenos
        if (!studyData.titulo || !studyData.centro || !studyData.nivel || !studyData.inicio || !studyData.final) {
            alert("Por favor, completa todos los campos.");
            return;
        }
         // Si se está editando un estudio, lo reemplaza; si no, lo agrega

        if (editingIndex !== null) {
            studies[editingIndex] = studyData;
        } else {
            studies.push(studyData);
        }
         // Guarda la lista de estudios actualizada en `localStorage`

        localStorage.setItem("studies", JSON.stringify(studies));
        renderStudies(); // Vuelve a mostrar la lista actualizada
        closeModalFunc();// Cierra el modal
    }

    // Eliminar un estudio
    function deleteStudy() {
        const studies = JSON.parse(localStorage.getItem("studies")) || [];
        if (editingIndex !== null && confirm("¿Seguro que quieres eliminar este estudio?")) {
            studies.splice(editingIndex, 1);
            localStorage.setItem("studies", JSON.stringify(studies));
            renderStudies();
            closeModalFunc();
        }
    }
    //Mostrar la lista de estudios
    function renderStudies() {
        studiesList.innerHTML = "";// Limpia la lista antes de actualizarla
        const studies = JSON.parse(localStorage.getItem("studies")) || [];

        studies.forEach((study, index) => {
            const studyItem = document.createElement("div");
            studyItem.classList.add("experience-item");
            studyItem.setAttribute("data-index", index);
            studyItem.style.display = "flex";
            studyItem.style.alignItems = "center";
            studyItem.style.justifyContent = "space-between";
            studyItem.style.padding = "8px";

            const studyContent = document.createElement("div");
            studyContent.innerHTML = `
               
                <strong >${study.titulo}</strong><br>
                <p>${study.centro}</p>
                <p>${study.nivel}</p>
                <p>${study.inicio} - ${study.final}</p>
            `;

            studyItem.appendChild(studyContent);

            // Solo agrega el ícono de edición a partir del segundo estudio
            if (index > 0) {
                const editIcon = document.createElement("img");
                editIcon.src = "img/pencil.svg";
                editIcon.alt = "Editar";
                editIcon.style.cursor = "pointer";
                editIcon.style.width = "22px";
                editIcon.addEventListener("click", () => openModal(true, index));

                studyItem.appendChild(editIcon);
            }

            studiesList.appendChild(studyItem);
        });

        // 📌 Mostrar el primer estudio en los campos de visualización
        if (studies.length > 0) {
            const firstStudy = studies[0];
            displayTitulo.textContent = firstStudy.titulo;
            displayCentro.textContent = firstStudy.centro;
            displayNivel.textContent = firstStudy.nivel;
            displayInicio.textContent = firstStudy.inicio;
            displayFinal.textContent = firstStudy.final;
        }
    }

    addButton.addEventListener("click", () => openModal(false));
    saveButton.addEventListener("click", saveStudy);
    deleteButton.addEventListener("click", deleteStudy);
    closeModal.addEventListener("click", closeModalFunc);
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            closeModalFunc();
        }
    });

    // 📌 Botón de edición general (arriba a la derecha) edita solo el primer estudio
    if (editButton) {
        editButton.addEventListener("click", () => {
            const studies = JSON.parse(localStorage.getItem("studies")) || [];
            if (studies.length > 0) {
                openModal(true, 0);
            } else {
                alert("No hay estudios para editar.");
            }
        });
    }

    renderStudies();
});

//Javascrip de idioma
document.addEventListener("DOMContentLoaded", function () {
    //Seleciona los elementos clave
    const openModal = document.getElementById("openModal");
    const closeIdiomaModal = document.getElementById("closeIdiomaModal");
    const modal = document.getElementById("modal");
    const saveButton = document.getElementById("save");
    
    const languageSelect = document.getElementById("language");
    const levelSelect = document.getElementById("level");
    const languagesList = document.getElementById("languages-list");

    // Mostrar modal
    openModal.addEventListener("click", function () {
        modal.style.display = "block";
    });

    // Ocultar modal con la "X"
    closeIdiomaModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Ocultar modal si se hace clic fuera de él
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // Función para agregar un idioma a la lista
    function addLanguage(language, level) {
        // Evitar duplicados
        const existingLanguages = document.querySelectorAll(".language-text");
        for (let item of existingLanguages) {
            if (item.textContent.includes(language) && item.textContent.includes(level)) {
                alert("Este idioma ya está agregado.");
                return;
            }
        }

        const newLanguage = document.createElement("div");
        newLanguage.classList.add("language-item");

        // Contenedor del texto
        const languageText = document.createElement("span");
        languageText.classList.add("language-text");
        languageText.innerHTML = `<span class="icon-check">✔</span> ${language} <small>(${level})</small>`;


        // Crear el botón de eliminar (-)
        const deleteIcon = document.createElement("span");
        deleteIcon.classList.add("delete-icon");
        deleteIcon.innerHTML = '<i class="bi bi-trash"></i>';
        
        // Evento para eliminar un solo idioma
        deleteIcon.addEventListener("click", function () {
            removeLanguage(language, level, newLanguage);
        });

        // Agregar elementos al contenedor principal
        newLanguage.appendChild(languageText);
        newLanguage.appendChild(deleteIcon);
        languagesList.appendChild(newLanguage);
    }

    // Guardar idioma
    saveButton.addEventListener("click", function () {
        const language = languageSelect.value;
        const level = levelSelect.value;

        if (language && level) {
            addLanguage(language, level);
            modal.style.display = "none";

            // Guardar en localStorage
            let savedLanguages = JSON.parse(localStorage.getItem("languages")) || [];
            savedLanguages.push({ language, level });
            localStorage.setItem("languages", JSON.stringify(savedLanguages));
        } else {
            alert("Selecciona un idioma y nivel");
        }
    });

    // Eliminar un solo idioma
    function removeLanguage(language, level, element) {
        element.remove(); // Elimina el elemento de la interfaz

        // Eliminar del localStorage
        let savedLanguages = JSON.parse(localStorage.getItem("languages")) || [];
        savedLanguages = savedLanguages.filter(item => item.language !== language || item.level !== level);
        localStorage.setItem("languages", JSON.stringify(savedLanguages));
    }

 

    // Cargar idiomas guardados en localStorage
    function loadLanguages() {
        let savedLanguages = JSON.parse(localStorage.getItem("languages")) || [];
        savedLanguages.forEach(item => {
            addLanguage(item.language, item.level);
        });
    }

    loadLanguages();
});

//JavaScrip de aptitud
document.addEventListener("DOMContentLoaded", function () {
    const openSkillModal = document.getElementById("openSkillModal");
    const closeSkillModal = document.getElementById("closeSkillModal");
    const skillModal = document.getElementById("skillModal");
    const saveSkillButton = document.getElementById("saveSkill");
    
    const skillInput = document.getElementById("skillInput");
    const skillsList = document.getElementById("skills-list");

    // Mostrar modal
    openSkillModal.addEventListener("click", function () {
        skillModal.style.display = "block";
    });

    // Ocultar modal con la "X"
    closeSkillModal.addEventListener("click", function () {
        skillModal.style.display = "none";
    });

    // Ocultar modal si se hace clic fuera de él
    window.addEventListener("click", function (event) {
        if (event.target === skillModal) {
            skillModal.style.display = "none";
        }
    });

    // Función para agregar una aptitud a la lista con botón de eliminar
    function addSkillToList(skill) {
        const newSkill = document.createElement("p");
        newSkill.innerHTML = `<span class="icon-check">✔</span> ${skill} `;

        // Crear botón de eliminar
        const deleteIcon = document.createElement("span");
        deleteIcon.classList.add("delete-icon1");
        deleteIcon.innerHTML = '<i class="bi bi-trash"></i>';
        
        
        // Evento para eliminar la aptitud
        deleteIcon.addEventListener("click", function () {
            newSkill.remove();

            // Eliminar del localStorage
            let savedSkills = JSON.parse(localStorage.getItem("skills")) || [];
            savedSkills = savedSkills.filter(s => s !== skill);
            localStorage.setItem("skills", JSON.stringify(savedSkills));
        });

        // Agregar el ícono de eliminar al elemento
        newSkill.appendChild(deleteIcon);
        skillsList.appendChild(newSkill);
    }

    // Guardar aptitud
    saveSkillButton.addEventListener("click", function () {
        const skill = skillInput.value.trim();

        if (skill) {
            addSkillToList(skill);
            skillModal.style.display = "none";
            skillInput.value = "";

            // Guardar en localStorage
            let savedSkills = JSON.parse(localStorage.getItem("skills")) || [];
            savedSkills.push(skill);
            localStorage.setItem("skills", JSON.stringify(savedSkills));
        } else {
            alert("Escribe una aptitud antes de guardar.");
        }
    });

    // Cargar aptitudes guardadas en localStorage
    function loadSkills() {
        skillsList.innerHTML = ""; // Limpiar lista antes de cargar
        let savedSkills = JSON.parse(localStorage.getItem("skills")) || [];
        savedSkills.forEach(skill => {
            addSkillToList(skill);
        });
    }

    loadSkills();
});
