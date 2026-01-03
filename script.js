const BASE_URL = "http://127.0.0.1:5001";

// Log Habit
function logHabit() {
    const habit = document.getElementById("habitInput").value;

    fetch(`${BASE_URL}/api/habits`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ habit })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("habitMsg").innerText = data.message || data.error;
        fetchHabits();
    });
}

// Fetch Habits
function fetchHabits() {
    fetch(`${BASE_URL}/api/habits`)
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("habitList");
        list.innerHTML = "";
        data.habits.forEach(h => {
            const li = document.createElement("li");
            li.textContent = `${h.text} (${h.category}) → Score: ${h.impact_score}`;
            list.appendChild(li);
        });
    });
}

// Green Score
function fetchScore() {
    fetch(`${BASE_URL}/api/score`)
    .then(res => res.json())
    .then(data => {
        document.getElementById("scoreData").innerHTML = `
            <p><b>Green Score:</b> ${data.green_score}</p>
            <p><b>Total Habits:</b> ${data.total_habits}</p>
            <p><b>Total Score:</b> ${data.total_score}</p>
        `;
    });
}

// Suggestions
function fetchSuggestions() {
    fetch(`${BASE_URL}/api/suggestions`)
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("suggestionsList");
        list.innerHTML = "";
        data.suggestions.forEach(s => {
            const li = document.createElement("li");
            li.textContent = s;
            list.appendChild(li);
        });
    });
}

// Agriculture Tips
function fetchAgriTips() {
    fetch(`${BASE_URL}/api/agriculture/tips`)
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("agriTips");
        list.innerHTML = "";
        data.tips.forEach(tip => {
            const li = document.createElement("li");
            li.textContent = tip;
            list.appendChild(li);
        });
    });
}

// Crop Recommendation
function getCropRecommendation() {
    const crop = document.getElementById("cropInput").value;

    fetch(`${BASE_URL}/api/agriculture/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ crop })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("cropResult").innerText =
            data.recommendation || data.error;
    });
}
