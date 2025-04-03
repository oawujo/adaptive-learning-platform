
import React, { useEffect, useState } from "react";
import {
  Line, Bar
} from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function LearnerDashboard({ userId = "oawujo" }) {
  const [history, setHistory] = useState([]);
  const [recommendation, setRecommendation] = useState(null);

  const API_BASE = "http://localhost:8000";

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(`${API_BASE}/history?user_id=${userId}`);
        const data = await res.json();
        setHistory(data.history || []);
      } catch (err) {
        console.error("Error fetching history:", err);
      }
    };

    const fetchRecommendation = async () => {
      try {
        const res = await fetch(`${API_BASE}/recommend`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: userId })
        });
        const data = await res.json();
        setRecommendation(data.recommended_topic);
      } catch (err) {
        console.error("Error fetching recommendation:", err);
      }
    };

    fetchHistory();
    fetchRecommendation();
  }, [userId]);

  const timestamps = history.map(h => new Date(h.timestamp).toLocaleString());
  const scores = history.map(h => h.score);
  const topics = [...new Set(history.map(h => h.topic))];
  const timeByTopic = topics.map(topic =>
    history
      .filter(h => h.topic === topic)
      .reduce((sum, entry) => sum + (parseInt(entry.time_spent) || 0), 0)
  );

  const scoreChartData = {
    labels: timestamps,
    datasets: [{
      label: "Score Over Time",
      data: scores,
      borderColor: "blue",
      backgroundColor: "lightblue",
      fill: false,
    }]
  };

  const timeChartData = {
    labels: topics,
    datasets: [{
      label: "Time Spent Per Topic (mins)",
      data: timeByTopic,
      backgroundColor: "orange"
    }]
  };

  return (
    <div style={{ marginTop: "2rem", padding: "1rem" }}>
      <h2>📊 Learner Dashboard</h2>

      <h3 style={{ marginTop: "1rem" }}>📈 Score Progress</h3>
      <Line data={scoreChartData} />

      <h3 style={{ marginTop: "2rem" }}>⏱ Time Spent by Topic</h3>
      <Bar data={timeChartData} />

      <h3 style={{ marginTop: "2rem" }}>📁 Learning History</h3>
      {history.length > 0 ? (
        <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Topic</th>
              <th>Score</th>
              <th>Level</th>
              <th>Content Type</th>
              <th>Time Spent (mins)</th>
            </tr>
          </thead>
          <tbody>
            {history.map((entry, idx) => (
              <tr key={idx}>
                <td>{new Date(entry.timestamp).toLocaleString()}</td>
                <td>{entry.topic}</td>
                <td>{entry.score}</td>
                <td>{entry.level}</td>
                <td>{entry.content_type}</td>
                <td>{entry.time_spent}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Loading history...</p>
      )}

      <h3 style={{ marginTop: "2rem" }}>🎯 Personalized Suggestion</h3>
      <div>
        {recommendation ? (
          <p>Your next recommended topic is: <strong>{recommendation}</strong></p>
        ) : (
          <p>Loading recommendation...</p>
        )}
      </div>
    </div>
  );
}
