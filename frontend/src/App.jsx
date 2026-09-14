import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('plugins', 'summarize');

    try {
      // Relativer Pfad! Vite leitet das automatisch an localhost:8002 weiter.
      const res = await axios.post('/api/v1/transcribe', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || "Netzwerkfehler");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>🎙️ STT AI Platform</h1>
      <p>Speech to text mit OpenAI Whisper-Base und Whisper Tiny </p>
      
      <div className="upload-box">
        <input type="file" accept="audio/*" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} disabled={loading || !file}>
          {loading ? 'Verarbeite...' : 'Transkribieren'}
        </button>
        {error && <p style={{color: 'red', marginTop: '1rem'}}>❌ {error}</p>}
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
