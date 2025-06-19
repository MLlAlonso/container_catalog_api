document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = window.location.origin;
    const API_VERSION_PATH = "/api/v1";
    const CONTAINERS_API_URL = `${API_BASE_URL}${API_VERSION_PATH}/containers`;

    // --- Elementos del DOM ---
    const containerListDiv = document.getElementById('containerList');
    const noResultsMessage = document.getElementById('noResultsMessage');

    // Formulario Añadir/Editar
    const addEditSection = document.getElementById('addEditSection');
    const showAddFormBtn = document.getElementById('showAddFormBtn');
    const cancelFormBtn = document.getElementById('cancelFormBtn');
    const containerForm = document.getElementById('containerForm');
    const formTitle = document.getElementById('formTitle');
    const containerIdInput = document.getElementById('containerId');
    const codeInput = document.getElementById('code');
    const typeInput = document.getElementById('type');
    const statusInput = document.getElementById('status');
    const currentLocationInput = document.getElementById('currentLocation');
    const ownerInput = document.getElementById('owner');

    // Mensajes de error de validación del formulario
    const codeError = document.getElementById('codeError');
    const typeError = document.getElementById('typeError');
    const statusError = document.getElementById('statusError');
    const currentLocationError = document.getElementById('currentLocationError');
    const ownerError = document.getElementById('ownerError');

    // Modal de Detalles
    const detailsModal = document.getElementById('detailsModal');
    const modalDetailsDiv = document.getElementById('modalDetails');
    const closeModalBtn = document.querySelector('.modal__close-button');

    // Modal de Confirmación Personalizado
    const confirmModal = document.getElementById('confirmModal');
    const confirmModalTitle = document.getElementById('confirmModalTitle');
    const confirmModalMessage = document.getElementById('confirmModalMessage');
    const confirmYesBtn = document.getElementById('confirmYesBtn');
    const confirmNoBtn = document.getElementById('confirmNoBtn');

    // Barra de Búsqueda
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');

    // --- Variables de Estado de la UI ---
    let isEditMode = false;
    let confirmActionCallback = null;
    let allContainers = []; 
    let currentSearchTerm = ''; 

    // --- Funciones de Interacción con la API ---
    async function fetchAllContainersAndDisplay() {
        containerListDiv.innerHTML = '<p>Cargando contenedores...</p>';
        noResultsMessage.style.display = 'none';

        try {
            const response = await fetch(CONTAINERS_API_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            allContainers = await response.json(); 
            renderAllContainersCards(allContainers); 
            filterAndDisplayContainers();
        } catch (error) {
            console.error('Error fetching containers:', error);
            containerListDiv.innerHTML = '<p class="error-message">Error al cargar los contenedores. Por favor, intente de nuevo más tarde.</p>';
        }
    }

//    Obtiene un contenedor específico por su ID
    async function fetchContainerById(id) {
        try {
            const response = await fetch(`${CONTAINERS_API_URL}/${id}`);
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error(`Contenedor con ID ${id} no encontrado.`);
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error fetching container with ID ${id}:`, error);
            alert(`Error: ${error.message}`);
            return null;
        }
    }

    // Guarda (crea o actualiza) un contenedor en la API.
    async function saveContainer(containerData, method, id = null) {
        let url = CONTAINERS_API_URL;
        if (method === 'PUT' && id) {
            url = `${CONTAINERS_API_URL}/${id}`;
        }

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(containerData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 409 && errorData.detail) {
                    throw new Error(errorData.detail);
                }
                if (response.status === 422 && errorData.detail) {
                    errorData.detail.forEach(err => {
                        const inputId = err.loc[1];
                        const errorElement = document.getElementById(`${inputId}Error`);
                        const inputElement = document.getElementById(inputId);
                        if (errorElement && inputElement) {
                            displayValidationError(inputElement, errorElement, err.msg);
                        }
                    });
                    throw new Error("Corrige los errores del formulario.");
                }
                throw new Error(`Error del servidor: ${response.status} - ${errorData.detail || response.statusText}`);
            }

            alert(`Contenedor ${method === 'POST' ? 'creado' : 'actualizado'} exitosamente.`);
            hideForm();
            await fetchAllContainersAndDisplay();
            return await response.json();
        } catch (error) {
            console.error('Error saving container:', error);
            alert(`No se pudo ${method === 'POST' ? 'crear' : 'actualizar'} el contenedor: ${error.message}`);
        }
    }

    // Elimina un contenedor
    async function performDeleteContainer(id) {
        try {
            const response = await fetch(`${CONTAINERS_API_URL}/${id}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error(`Contenedor con ID ${id} no encontrado para eliminar.`);
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            alert('Contenedor eliminado exitosamente.');
            await fetchAllContainersAndDisplay();
        } catch (error) {
            console.error('Error deleting container:', error);
            alert(`No se pudo eliminar el contenedor: ${error.message}`);
        }
    }

    /**
     * Funciones de Renderizado y Lógica de Búsqueda
     * Renderiza todas las tarjetas de contenedores en el DOM.
     * @param {Array<Object>} containers - La lista de contenedores a renderizar.
     */
    function renderAllContainersCards(containers) {
        containerListDiv.innerHTML = '';
        if (containers.length === 0) {
            return;
        }

        containers.forEach(container => {
            const card = document.createElement('div');
            card.className = 'container-card';
            card.dataset.id = container.id;
            card.innerHTML = `
                <div class="container-card__header">
                    <h3 class="container-card__code">${container.code}</h3>
                </div>
                <div class="container-card__details">
                    <p class="container-card__detail">Tipo: <span>${container.type}</span></p>
                    <p class="container-card__detail">Estado: <span>${container.status}</span></p>
                    <p class="container-card__detail">Ubicación: <span>${container.current_location}</span></p>
                    <p class="container-card__detail">Propietario: <span>${container.owner}</span></p>
                    <p class="container-card__detail">Actualizado: <span>${new Date(container.last_updated).toLocaleString()}</span></p>
                </div>
                <div class="container-card__actions">
                    <button class="button button--secondary button--view" data-id="${container.id}">Ver</button>
                    <button class="button button--primary button--edit" data-id="${container.id}">Editar</button>
                    <button class="button button--danger button--delete" data-id="${container.id}">Eliminar</button>
                </div>
            `;
            containerListDiv.appendChild(card);
        });

        attachCardButtonListeners();
    }

    // Filtra los contenedores
    function filterAndDisplayContainers() {
        const term = currentSearchTerm.toLowerCase();
        let resultsFound = 0;

        document.querySelectorAll('.container-card').forEach(card => {
            const containerCode = card.querySelector('.container-card__code').textContent.toLowerCase();
            const containerDetails = card.querySelector('.container-card__details').textContent.toLowerCase();

            if (containerCode.includes(term) || containerDetails.includes(term)) {
                card.style.display = 'flex'; 
                resultsFound++;
            } else {
                card.style.display = 'none';
            }
        });

        if (resultsFound === 0 && term !== '') {
            noResultsMessage.style.display = 'block';
        } else {
            noResultsMessage.style.display = 'none';
        }

        if (allContainers.length === 0 && term === '') {
            containerListDiv.innerHTML = '<p>No hay contenedores registrados aún. ¡Crea uno!</p>';
        } else if (allContainers.length > 0 && resultsFound === 0 && term !== '') {
        } else if (allContainers.length > 0 && resultsFound > 0 && term !== '') {
            containerListDiv.style.display = 'grid';
        } else if (allContainers.length > 0 && term === '') {
            containerListDiv.style.display = 'grid';
        }
    }

    function attachCardButtonListeners() {
        document.querySelectorAll('.button--view').forEach(button => {
            button.addEventListener('click', (e) => showContainerDetails(e.target.dataset.id));
        });
        document.querySelectorAll('.button--edit').forEach(button => {
            button.addEventListener('click', (e) => populateFormForEdit(e.target.dataset.id));
        });
        document.querySelectorAll('.button--delete').forEach(button => {
            button.addEventListener('click', (e) => {
                const containerId = e.target.dataset.id;
                showConfirmModal(
                    'Confirmar Eliminación',
                    `¿Estás seguro de que quieres eliminar el contenedor con ID **${containerId}**? Esta acción no se puede deshacer.`,
                    () => performDeleteContainer(containerId)
                );
            });
        });
    }

    // --- Funciones de UI ---
    function showForm(edit = false) {
        addEditSection.style.display = 'block';
        isEditMode = edit;
        formTitle.textContent = edit ? 'Editar Contenedor' : 'Añadir Nuevo Contenedor';
        if (!edit) {
            containerForm.reset();
            containerIdInput.value = '';
        }
        clearValidationErrors();
        addEditSection.scrollIntoView({ behavior: 'smooth' });
    }

    function hideForm() {
        addEditSection.style.display = 'none';
        containerForm.reset();
        containerIdInput.value = '';
        isEditMode = false;
        clearValidationErrors();
    }

    async function populateFormForEdit(id) {
        const container = await fetchContainerById(id);
        if (container) {
            containerIdInput.value = container.id;
            codeInput.value = container.code;
            typeInput.value = container.type;
            statusInput.value = container.status;
            currentLocationInput.value = container.current_location;
            ownerInput.value = container.owner;
            showForm(true);
        }
    }

    async function showContainerDetails(id) {
        const container = await fetchContainerById(id);
        if (container) {
            modalDetailsDiv.innerHTML = `
                <p><strong>ID:</strong> ${container.id}</p>
                <p><strong>Código:</strong> ${container.code}</p>
                <p><strong>Tipo:</strong> ${container.type}</p>
                <p><strong>Estado:</strong> ${container.status}</p>
                <p><strong>Ubicación Actual:</strong> ${container.current_location}</p>
                <p><strong>Propietario:</strong> ${container.owner}</p>
                <p><strong>Última Actualización:</strong> ${new Date(container.last_updated).toLocaleString()}</p>
            `;
            detailsModal.style.display = 'flex';
        }
    }

    // --- Funciones de Validación de Formulario ---
    function validateForm() {
        let isValid = true;
        clearValidationErrors();

        const fields = [
            { input: codeInput, error: codeError, name: 'Código' },
            { input: typeInput, error: typeError, name: 'Tipo' },
            { input: statusInput, error: statusError, name: 'Estado' },
            { input: currentLocationInput, error: currentLocationError, name: 'Ubicación Actual' },
            { input: ownerInput, error: ownerError, name: 'Propietario' },
        ];

        fields.forEach(field => {
            if (field.input.value.trim() === '') {
                displayValidationError(field.input, field.error, `${field.name} es requerido.`);
                isValid = false;
            } else {
                if (field.input.value.length > 255) {
                    displayValidationError(field.input, field.error, `El ${field.name.toLowerCase()} no debe exceder 255 caracteres.`);
                    isValid = false;
                }
            }
        });
        return isValid;
    }

    function displayValidationError(inputElement, errorElement, message) {
        inputElement.classList.add('is-invalid');
        errorElement.textContent = message;
    }

    function clearValidationErrors() {
        document.querySelectorAll('.form__input').forEach(input => {
            input.classList.remove('is-invalid');
        });
        document.querySelectorAll('.form__error-message').forEach(error => {
            error.textContent = '';
        });
    }

    // --- Funciones del Modal Personalizado ---
    function showConfirmModal(title, message, callback) {
        confirmModalTitle.innerHTML = title;
        confirmModalMessage.innerHTML = message;
        confirmActionCallback = callback;
        confirmModal.style.display = 'flex';
    }

    function hideConfirmModal() {
        confirmModal.style.display = 'none';
        confirmActionCallback = null;
    }

    // --- Event Listeners Globales ---

    showAddFormBtn.addEventListener('click', () => showForm(false));
    cancelFormBtn.addEventListener('click', hideForm);

    containerForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (!validateForm()) {
            return;
        }

        const containerData = {
            code: codeInput.value,
            type: typeInput.value,
            status: statusInput.value,
            current_location: currentLocationInput.value,
            owner: ownerInput.value,
        };

        if (isEditMode) {
            showConfirmModal(
                'Confirmar Actualización',
                `¿Estás seguro de que quieres guardar los cambios en el contenedor con ID **${containerIdInput.value}**?`,
                async () => {
                    await saveContainer(containerData, 'PUT', containerIdInput.value);
                }
            );
        } else {
            await saveContainer(containerData, 'POST');
        }
    });

    // Eventos de la barra de búsqueda
    searchBtn.addEventListener('click', () => {
        currentSearchTerm = searchInput.value.trim();
        filterAndDisplayContainers();
    });

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });

    // Cerrar el modal de detalles
    closeModalBtn.addEventListener('click', () => {
        detailsModal.style.display = 'none';
    });

    // Ocultar cualquier modal al hacer clic fuera del contenido
    window.addEventListener('click', (event) => {
        if (event.target == detailsModal) {
            detailsModal.style.display = 'none';
        }
        if (event.target == confirmModal) {
            hideConfirmModal();
        }
    });

    confirmYesBtn.addEventListener('click', () => {
        if (confirmActionCallback) {
            confirmActionCallback();
        }
        hideConfirmModal();
    });

    confirmNoBtn.addEventListener('click', hideConfirmModal);

    fetchAllContainersAndDisplay();
});