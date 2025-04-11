import React, { useState } from "react";

export default function LearningLogger() {
  const [formData, setFormData] = useState({
    user_id: "",
    action: "quiz_completed",
    score: "",
    content_type: "video",
    time_spent: "",
    topic: "Photosynthesis",
    level: "beginner",
    style: "text"
  });

  const [response, setResponse] = useState(null);
  const [generatedContent, setGeneratedContent] = useState("");
  const [error, setError] = useState("");

  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting form:", formData);

    setError("");
    try {
      const logRes = await fetch(`${API_BASE}/log`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!logRes.ok) {
        const text = await logRes.text();
        throw new Error(`Log error: ${logRes.status} - ${text}`);
      }

      const logData = await logRes.json();
      console.log("Log response:", logData);
      setResponse(logData);
    } catch (err) {
      console.error("Failed to log data:", err);
      setError(`Logging failed: ${err.message}`);
    }

    try {
      const genRes = await fetch(`${API_BASE}/generate-content`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!genRes.ok) {
        const text = await genRes.text();
        throw new Error(`Content error: ${genRes.status} - ${text}`);
      }

      const genData = await genRes.json();
      console.log("Generated content:", genData);
      setGeneratedContent(genData.generated_content);
    } catch (err) {
      console.error("Failed to fetch content:", err);
      setError(`Content fetch failed: ${err.message}`);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: "1rem" }}>
        <input name="user_id" placeholder="User ID" value={formData.user_id} onChange={handleChange} />
        <select name="action" value={formData.action} onChange={handleChange}>
          <option value="quiz_completed">Quiz Completed</option>
          <option value="lesson_started">Lesson Started</option>
          <option value="lesson_completed">Lesson Completed</option>
          <option value="feedback_submitted">Feedback Submitted</option>
        </select>
        <input name="score" type="number" placeholder="Score" value={formData.score} onChange={handleChange} />
        <select name="content_type" value={formData.content_type} onChange={handleChange}>
          <option value="video">Video</option>
          <option value="text">Text</option>
          <option value="interactive">Interactive</option>
          <option value="quiz">Quiz</option>
        </select>
        <input name="time_spent" type="number" placeholder="Time Spent (mins)" value={formData.time_spent} onChange={handleChange} />
        <input name="topic" placeholder="Learning Topic" value={formData.topic} onChange={handleChange} />
        <select name="level" value={formData.level} onChange={handleChange}>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        <select name="style" value={formData.style} onChange={handleChange}>
          <option value="text">Text</option>
          <option value="visual">Visual</option>
          <option value="interactive">Interactive</option>
        </select>
        <button type="submit">Submit</button>
      </form>

      {response?.logged?.timestamp && (
        <div style={{ marginTop: "1rem", color: "green" }}>
          ✅ Action logged at {response.logged.timestamp}
        </div>
      )}

      {error && (
        <div style={{ marginTop: "1rem", color: "red" }}>
          ❌ {error}
        </div>
      )}

      {generatedContent && (
        <div
          style={{
            marginTop: "2rem",
            padding: "1rem",
            border: "1px solid #ccc",
            maxHeight: "500px",
            overflowY: "auto",
            whiteSpace: "pre-wrap",
            backgroundColor: "#f9f9f9",
            fontFamily: "monospace"
          }}
        >
          <h3>📘 Generated Lesson:</h3>
          <pre>{generatedContent}</pre>
        </div>
      )}
    </div>
  );
}