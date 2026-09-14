import os

files = {
    "src/App.jsx": """import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('plugins', 'summarize');

    try {
      const res = await axios.post('http://localhost:8000/api/v1/transcribe', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data);
    } catch (error) {
      console.error(error);
      alert("Fehler bei der Transkription");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>🎙️ STT AI Platform</h1>
      <p>Junior AI Engineer Portfolio Projekt</p>
      
      <div className="upload-box">
        <input type="file" accept="audio/*" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} disabled={loading || !file}>
          {loading ? 'Verarbeite...' : 'Transkribieren'}
        </button>
      </div>

      {result && (
        <div className="result-box">
          <h3>Ergebnis:</h3>
          <p><strong>Text:</strong> {result.text}</p>
          <p><strong>Modell:</strong> {result.model_used}</p>
          <p><strong>Zeit:</strong> {result.processing_time_ms.toFixed(2)} ms</p>
          {result.plugin_results && (
            <div>
              <strong>Plugins:</strong>
              <pre>{JSON.stringify(result.plugin_results, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
""",

    "src/App.css": """.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}
.upload-box {
  margin: 2rem 0;
  padding: 2rem;
  border: 2px dashed #ccc;
  border-radius: 10px;
}
button {
  margin-top: 1rem;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:disabled { background: #ccc; }
.result-box {
  text-align: left;
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 2rem;
}
"""
}

for filepath, content in files.items():
    with open(filepath, "w") as f:
        f.write(content)
    print(f"✅ Überschrieben: {filepath}")

print("\\n🎉 Frontend ist jetzt startklar!")
