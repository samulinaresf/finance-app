/*Creando las variables*/ 
const dropArea = document.getElementById('drop-area');
const fileElement = document.getElementById('file-element');
const filePreview = document.getElementById('file-preview');
const deleteElement = document.getElementById('delete-element');
const uploadElement = document.getElementById('upload-element');
const dropText = document.getElementById('drop-text')
let currentFile = null;

if (dropArea){
    /*Activando el input al hacer click en el área de drop*/
    dropArea.addEventListener('click', ()=>{
        fileElement.click();
    });

    /*Estilizando el área al arrastrar un archivo por encima*/
    dropArea.addEventListener('dragover', (event)=>{
        event.preventDefault();
        dropArea.classList.add('drag-over')
    });

    /*Quitando estilo cuando el archivo sale del área*/
    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('drag-over');
    });

    /*Capturando el archivo soltado en el área y mostrándolo*/
    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('drag-over');
        const files = event.dataTransfer.files;
        showFile(files[0]);
    });
}

/*Mostrando el archivo si se selecciona desde el explorador*/
if (fileElement){
    fileElement.addEventListener('change', (event) => {
        showFile(event.target.files[0]);
    });
}

/*Creando la funcionalidad de mostrar archivo*/
function showFile(file) {
    currentFile = file
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
        filePreview.innerHTML = `<p>Archivo cargado: <strong>${file.name}</strong></p>`;
    }
    dropText.style.display = "none"
    console.log("Archivo subido:", file.name);
}

/*Creando la funcionalidad del botón de eliminar*/
if (deleteElement){    
    deleteElement.addEventListener('click', () => {
        fileElement.value = "";
        filePreview.innerHTML = "";
        currentFile = null; 
        dropText.style.display = "block" 
        console.log("Botón de eliminar pulsado");
    })
}

/*Creando la funcionalidad del botón subir*/
if (uploadElement){
    uploadElement.addEventListener('click', () => {
        var formData = new FormData();
        formData.append("fileName", currentFile.name);       // Añadimos el nombre del archivo
        formData.append("uploadDate", Date.now());           // Añadimos la fecha actual
        formData.append("file", currentFile);                // Añadimos el archivo como tal
    
        var request = new XMLHttpRequest();
        request.open("POST", "/uploads");                    // Enviamos al endpoint Flask
        request.send(formData);
        
    
        /*Manejando la respuesta del servidor*/
        request.onload = () => {
            if (request.status === 200) {
                const response = JSON.parse(request.responseText);
                window.location.href = `/graph/${encodeURIComponent(response.fileName)}`;
            } else {
                const response = JSON.parse(request.responseText);
                const errorMessage = response.message || "Archivo no válido";
                showError(errorMessage);
            }
        }
    });
}

function showError(message) {
    let errorDiv = document.getElementById('error-message');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'error-message';
        dropArea.parentNode.insertBefore(errorDiv, dropArea.nextSibling);
    }
    errorDiv.textContent = message;
}


/*Manipulando los gráficos*/
const graphIncomes = document.getElementById('graph-incomes')
const graphExpenses = document.getElementById('graph-expenses')
const graphComparison = document.getElementById('graph-comparison')
const buttonIncomes = document.getElementById('button-incomes')
const buttonExpenses = document.getElementById('button-expenses')
const buttonComparison = document.getElementById('button-comparison')
const deleteCsv = document.getElementById('delete-csv')

if (buttonIncomes && graphIncomes) {
    buttonIncomes.addEventListener('click', () => {
        graphIncomes.style.display = 'flex';
        graphExpenses.style.display = 'none';
        graphComparison.style.display = 'none';
        graphComparison.style.justifyContent= 'center'
        graphComparison.style.alignItems = 'center'
        graphComparison.style.marginLeft = 'auto'
        graphComparison.style.marginRight = 'auto'
        graphComparison.style.marginTop = '20px'
        graphComparison.style.width = '100%'
        console.log("Botón Ingresos pulsado.")
    });
}

if (buttonExpenses && graphExpenses) {
    buttonExpenses.addEventListener('click', () => {
        graphIncomes.style.display = 'none';
        graphExpenses.style.display = 'flex';
        graphComparison.style.display = 'none';
        graphComparison.style.justifyContent= 'center'
        graphComparison.style.alignItems = 'center'
        graphComparison.style.marginLeft = 'auto'
        graphComparison.style.marginRight = 'auto'
        graphComparison.style.marginTop = '20px'
        graphComparison.style.width = '100%'
        console.log("Botón Gastos pulsado.")
    });
}

if (buttonComparison && graphComparison) {
    buttonComparison.addEventListener('click', () => {
        graphIncomes.style.display = 'none';
        graphExpenses.style.display = 'none';
        graphComparison.style.display = 'flex';
        graphComparison.style.justifyContent= 'center'
        graphComparison.style.alignItems = 'center'
        graphComparison.style.marginLeft = 'auto'
        graphComparison.style.marginRight = 'auto'
        graphComparison.style.marginTop = '20px'
        graphComparison.style.width = '100%'
        console.log("Botón Comparativa pulsado.")
    });
}

if(deleteCsv){
    deleteCsv.addEventListener('click', () => {
        var formData = new FormData();
        formData.append("fileName",uploadedFileName);       // Añadimos el nombre del archivo
    
        var request = new XMLHttpRequest();
        request.open("POST", "/delete");                    // Enviamos al endpoint Flask
        request.send(formData);
        
        request.onload = () => {
            if (request.status === 200) {
                window.location.href = "/";
            } else {
                console.log("Error al eliminar el archivo.");
            }
        }
    })};


