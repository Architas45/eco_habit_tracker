const SUGGESTIONS_API = "http://127.0.0.1:5000/api/suggestions";

fetch(SUGGESTIONS_API)
    .then(response => response.json())
    .then(data => {

        // Personalized status
        document.getElementById("personalizedStatus").innerText =
            data.personalized ? "Yes" : "No";

        const container = document.getElementById("suggestionsContainer");

        data.suggestions.forEach(suggestion => {
            const card = document.createElement("div");
            card.className = "card";

            card.innerHTML = `
                <p><b>Suggestion:</b> ${suggestion.text}</p>
                <p><b>Category:</b> ${suggestion.category}</p>
                <p><b>Difficulty:</b> ${suggestion.difficulty}</p>
                <p><b>Reason:</b> ${suggestion.reason}</p>
            `;

            container.appendChild(card);
        });
    })
    .catch(error => {
        alert("Failed to load suggestions");
        console.error(error);
    });
