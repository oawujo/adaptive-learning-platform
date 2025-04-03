
import React from "react";
import LearningLogger from "./components/LearningLogger";
import LearnerDashboard from "./components/LearnerDashboard"; // ✅ this line is critical

function App() {
  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Adaptive Learning Platform</h1>
      <LearningLogger />
      <LearnerDashboard userId="oawujo" /> {/* ✅ render the dashboard */}
    </div>
  );
}

export default App;
