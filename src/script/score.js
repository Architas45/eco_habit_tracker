const SCORE_API = "http://127.0.0.1:5000/api/score";

fetch(SCORE_API)
    .then(response => response.json())
    .then(data => {

        document.getElementById("greenScore").innerText = data.green_score;
        document.getElementById("totalScore").innerText = data.total_score;
        document.getElementById("totalHabits").innerText = data.total_habits;

        const breakdownList = document.getElementById("breakdownList");

        for (let category in data.score_breakdown) {
            const item = data.score_breakdown[category];

            const li = document.createElement("li");
            li.innerHTML = `
                <b>${category}</b><br>
                Total Score: ${item.total_score}<br>
                Average Score: ${item.avg_score}<br>
                Habit Count: ${item.count}
            `;
            breakdownList.appendChild(li);
        }
    })
    .catch(error => {
        alert("Failed to load green score");
        console.error(error);
    });
