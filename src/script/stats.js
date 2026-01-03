const STATS_API = "http://127.0.0.1:5000/api/stats";

fetch(STATS_API)
    .then(response => response.json())
    .then(data => {
        const stats = data.stats;

        // Summary
        document.getElementById("totalHabits").innerText = stats.total_habits;
        document.getElementById("avgScore").innerText = stats.avg_daily_score;

        // Categories
        const categoryList = document.getElementById("categoryList");
        for (let category in stats.categories) {
            const li = document.createElement("li");
            li.innerText = `${category} : ${stats.categories[category]} habit(s)`;
            categoryList.appendChild(li);
        }

        // Trend
        document.getElementById("trend").innerText =
            stats.improvement_trend.trend;

        document.getElementById("trendPercent").innerText =
            stats.improvement_trend.trend_percentage + "%";

        document.getElementById("weeklyChange").innerText =
            stats.improvement_trend.weekly_change;

        // Top habits
        const topHabits = document.getElementById("topHabits");
        stats.top_habits.forEach(habit => {
            const li = document.createElement("li");
            li.innerText = `${habit.text} (${habit.category}) → Score: ${habit.impact_score}`;
            topHabits.appendChild(li);
        });
    })
    .catch(err => {
        alert("Failed to load statistics");
        console.error(err);
    });
