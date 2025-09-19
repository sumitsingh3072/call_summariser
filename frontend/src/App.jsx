import React, { useState } from 'react'

export default function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  function onFileChange(ev) {
    setFile(ev.target.files[0] || null)
    setResult(null)
    setError(null)
  }

  async function onSubmit(ev) {
    ev.preventDefault()
    setError(null)

    if (!file) {
      setError('Please select a .txt file to upload.')
      return
    }

    const form = new FormData()
    form.append('file', file)

    try {
      setLoading(true)
      setResult(null)

      const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const resp = await fetch(`${API_BASE.replace(/\/$/, '')}/analyze`, {
        method: 'POST',
        body: form,
      })

      if (!resp.ok) {
        const body = await resp.json().catch(() => ({}))
        throw new Error(body.detail || `Server responded with ${resp.status}`)
      }

      const data = await resp.json()
      setResult(data)
    } catch (err) {
      setError(err.message || String(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="header">
        <div className="logo">CS</div>
        <div>
          <h1>Call Summariser</h1>
          <div className="subtle">Upload a transcript and get a concise summary + sentiment</div>
        </div>
      </div>

      <form onSubmit={onSubmit} className="upload-form">
        <label htmlFor="file" className="subtle">Transcript (.txt)</label>
        <input id="file" type="file" accept=".txt,text/plain" onChange={onFileChange} />
        <button type="submit" className="magic-btn" disabled={loading}>{loading ? 'Analyzing...' : 'Analyze'}</button>
      </form>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h2>Analysis Result</h2>
          <div className="field">
            <strong>Summary:</strong>
            <p>{result.summary}</p>
          </div>
          <div className="field">
            <strong>Sentiment:</strong>
            <p>{result.sentiment}</p>
          </div>
          <details className="transcript">
            <summary>Original Transcript (click to expand)</summary>
            <pre>{result.transcript}</pre>
          </details>
        </div>
      )}

      <div className="note">Note: Backend must be running at <code>http://localhost:8000</code></div>
    </div>
  )
}
