import React, { useEffect, useState } from "react";

export default function LearnerDashboard({ userId }) {
  const [history, setHistory] = useState([]);
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState("");

  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    if (!userId) return;

    const fetchHistory = async () => {
      try {
        const res = await fetch(`${API_BASE}/history?user_id=${userId}`);
        if (!res.ok) {
          const text = await res.text();
          throw new Error(`History fetch failed: ${res.status} - ${text}`);
        }
        const data = await res.json();
        setHistory(data.logs || []);
      } catch (err) {
        console.error("Error fetching history:", err);
        setError(err.message);
      }
    };

    const fetchRecommendation = async () => {
      try {
        const res = await fetch(`${API_BASE}/recommend`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: userId }),
        });
        if (!res.ok) {
          const text = await res.text();
          throw new Error(`Recommendation fetch failed: ${res.status} - ${text}`);
        }
        const data = await res.json();
        setRecommendation(data);
      } catch (err) {
        console.error("Error fetching recommendation:", err);
        setError(err.message);
      }
    };

    fetchHistory();
    fetchRecommendation();
  }, [userId]);

  return (
    <div style={{ marginTop: "2rem", padding: "1rem", backgroundColor: "#f4f4f4" }}>
      <h2>📊 Learner Dashboard</h2>

      {error && (
        <div style={{ color: "red", marginBottom: "1rem" }}>
          ❌ Error: {error}
        </div>
      )}

      <div>
        <h3>📁 Learning History</h3>
        {history.length === 0 ? (
          <p>No history found.</p>
        ) : (
          <ul>
            {history.map((log, index) => (
              <li key={index}>
                [{log.timestamp}] {log.action} on "{log.topic}" ({log.level}) - {log.score || "N/A"} points
              </li>
            ))}
          </ul>
        )}
      </div>

      <div style={{ marginTop: "1rem" }}>
        <h3>🔮 Recommended Next Lesson</h3>
        {recommendation ? (
          <p>
            <strong>{recommendation.topic}</strong> at <em>{recommendation.level}</em> level
          </p>
        ) : (
          <p>No recommendation available.</p>
        )}
      </div>
    </div>
  );
}

