let predictions = [];
let currentPage = 1;
const recordsPerPage = 5;

async function uploadFile() {
    const fileInput = document.getElementById('csvFile');
    const resultDiv = document.getElementById('predictionsContainer');
    
    if (fileInput.files.length === 0) {
        resultDiv.innerHTML = "Please select a CSV file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch('/predict/', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.status_code === 200) {
            predictions = data.predictions;
            currentPage = 1;
            displayPage(currentPage);
            setupPagination();
        } else {
            resultDiv.innerHTML = "Error: " + data.detail;
        }
    } catch (error) {
        resultDiv.innerHTML = "An error occurred: " + error.detail;
    }
}

function displayPage(page) {
    const container = document.getElementById('predictionsContainer');
    container.innerHTML = ''; // Clear previous content

    const start = (page - 1) * recordsPerPage;
    const end = start + recordsPerPage;
    const pagePredictions = predictions.slice(start, end);

    pagePredictions.forEach(prediction => {
        const box = document.createElement('div');
        box.className = 'prediction-box';

        const message = `
            <h3>Dear ${prediction.Name}</h3>
            <p>Your credit score is <strong>${prediction.Score}</strong>.</p>
            ${prediction.Qualified_for_loan ? 
                '<p>Congratulations! You are eligible for a loan.</p>' : 
                '<p>Unfortunately, your score is below our limit, and you are not eligible for a loan.</p>'}
        `;
        box.innerHTML = message;
        container.appendChild(box);
    });
}

function setupPagination() {
    const paginationDiv = document.getElementById('pagination');
    paginationDiv.innerHTML = ''; // Clear previous pagination

    const totalPages = Math.ceil(predictions.length / recordsPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const pageLink = document.createElement('a');
        pageLink.innerText = i;
        pageLink.href = '#';
        pageLink.className = (i === currentPage) ? 'active' : '';
        pageLink.onclick = function (event) {
            event.preventDefault();
            currentPage = i;
            displayPage(currentPage);
            setupPagination();
        };
        paginationDiv.appendChild(pageLink);
    }
}
