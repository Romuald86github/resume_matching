document.getElementById('matchForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const resume = document.getElementById('resume').value;
    const job = document.getElementById('job').value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ resume: resume, job: job }),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<p>Similarity: ${data.similarity}</p><p>Match: ${data.match}</p>`;
    })
    .catch(error => console.error('Error:', error));
});
