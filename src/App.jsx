import React, { useState } from "react";
import "./App.css";

function App() {
  const [form, setForm] = useState({
    Gender: "",
    Age: "",
    Occupation: "",
    "Sleep Duration": "",
    "Physical Activity Level": "",
    "Stress Level": "",
    "BMI Category": "",
    "Blood Pressure": "",
    "Heart Rate": "",
    "Daily Steps": "",
    "Sleep Disorder": "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Field configurations for better UX - matching training data exactly
  const fieldConfig = {
    Gender: { type: "select", options: ["Male", "Female"] },
    Age: { type: "number", min: 1, max: 120, placeholder: "e.g., 25" },
    Occupation: { type: "select", options: ["Smit","Software Engineer", "Doctor","Businessman", "Sales Representative", "Teacher", "Nurse", "Engineer", "Accountant", "Scientist", "Lawyer", "Salesperson", "Manager"] },
    "Sleep Duration": { type: "number", min: 1, max: 24, step: 0.1, placeholder: "Hours (e.g., 7.5)" },
    "Physical Activity Level": { type: "number", min: 0, max: 100, placeholder: "Minutes per day (e.g., 60)" },
    "Stress Level": { type: "range", min: 1, max: 10, placeholder: "1-10 scale" },
    "BMI Category": { type: "select", options: ["Normal Weight", "Normal", "Overweight", "Obese"] },
    "Blood Pressure": { type: "text", placeholder: "e.g., 120/80" },
    "Heart Rate": { type: "number", min: 30, max: 200, placeholder: "BPM (e.g., 72)" },
    "Daily Steps": { type: "number", min: 0, max: 50000, placeholder: "Steps (e.g., 8000)" },
    "Sleep Disorder": { type: "select", options: ["None", "Sleep Apnea", "Insomnia"] },
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Prediction failed. Make sure your backend is running.");
    }
    setLoading(false);
  };

  const renderField = (key) => {
    const config = fieldConfig[key];
    const commonProps = {
      name: key,
      value: form[key],
      onChange: handleChange,
      required: true,
      className: "form-input"
    };

    switch (config.type) {
      case "select":
        return (
          <select {...commonProps}>
            <option value="">Select {key}</option>
            {config.options.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        );
      case "range":
        return (
          <div className="range-container">
            <input
              type="range"
              {...commonProps}
              min={config.min}
              max={config.max}
              className="form-range"
            />
            <span className="range-value">{form[key] || config.min}</span>
          </div>
        );
      default:
        return (
          <input
            type={config.type || "text"}
            {...commonProps}
            min={config.min}
            max={config.max}
            step={config.step}
            placeholder={config.placeholder}
          />
        );
    }
  };

  const isFormValid = Object.values(form).every(value => value !== "");

  return (
    <div className="app-container">
      <div className="background-decoration">
        <div className="moon"></div>
        <div className="stars"></div>
      </div>
      
      <div className="main-content">
        <header className="app-header">
          <div className="logo-container">
            <span className="logo-icon">🌙</span>
            <h1 className="app-title">SleepBuddy</h1>
          </div>
          <p className="app-subtitle">Discover your sleep quality with AI-powered insights</p>
        </header>

        <div className="form-container">
          <div className="form-grid">
            {Object.keys(form).map((key) => (
              <div key={key} className="form-group">
                <label className="form-label">{key}</label>
                {renderField(key)}
              </div>
            ))}
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading || !isFormValid}
            className={`predict-button ${loading ? 'loading' : ''}`}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing Sleep Pattern...
              </>
            ) : (
              <>
                <span className="button-icon">✨</span>
                Predict Sleep Quality
              </>
            )}
          </button>
        </div>

        {result && (
          <div className="results-container">
            <div className="results-header">
              <h3 className="results-title">
                <span className="results-icon">🔮</span>
                Sleep Quality Prediction
              </h3>
              <div className="prediction-badge">
                {result.prediction}
              </div>
            </div>
            
            <div className="confidence-section">
              <h4 className="confidence-title">Confidence Levels</h4>
              <div className="confidence-bars">
                {Object.entries(result.probabilities).map(([label, prob]) => (
                  <div key={label} className="confidence-item">
                    <div className="confidence-label">
                      <span>{label}</span>
                      <span className="confidence-percentage">{Math.round(prob * 100)}%</span>
                    </div>
                    <div className="confidence-bar">
                      <div 
                        className="confidence-fill" 
                        style={{ width: `${prob * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
