document.addEventListener("DOMContentLoaded", () => {
    loadCandidates();
    loadResults();

    document.getElementById("voteForm").addEventListener("submit", function(event) {
        event.preventDefault();
        const candidate = document.getElementById("candidates").value;

        fetch("/vote", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ candidate: candidate })
        })
        .then(response => response.text())  // First get raw text
        .then(text => {
            try {
                return JSON.parse(text);  // Attempt to parse JSON
            } catch (error) {
                console.error("Invalid JSON response:", text);
                throw error;
            }
        })
        .then(data => {
            alert(data.message);
            loadResults();
        })
        .catch(error => console.error("Error voting:", error));
    });

    document.getElementById("addCandidateForm").addEventListener("submit", function(event) {
        event.preventDefault();
        const newCandidate = document.getElementById("newCandidate").value;

        fetch("/add_candidate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newCandidate })
        })
        .then(response => response.text())  // First get raw text
        .then(text => {
            try {
                return JSON.parse(text);  // Attempt to parse JSON
            } catch (error) {
                console.error("Invalid JSON response:", text);
                throw error;
            }
        })
        .then(data => {
            alert(data.message);
            loadCandidates();
        })
        .catch(error => console.error("Error adding candidate:", error));
    });
});

// Load Candidates from Backend
function loadCandidates() {
    fetch("/candidates")
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById("candidates");
            select.innerHTML = "";
            data.forEach(candidate => {
                const option = document.createElement("option");
                option.value = candidate.name;
                option.textContent = candidate.name;
                select.appendChild(option);
            });
        })
        .catch(error => console.error("Error loading candidates:", error));
}

// Load Results from Backend
function loadResults() {
    fetch("/results")
        .then(response => response.json())
        .then(data => {
            const resultsTable = document.getElementById("results");
            resultsTable.innerHTML = "";
            data.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `<td>${row.name}</td><td>${row.votes}</td>`;
                resultsTable.appendChild(tr);
            });
        })
        .catch(error => console.error("Error loading results:", error));
}
