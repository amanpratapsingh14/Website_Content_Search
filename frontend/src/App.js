import React, { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showHtml, setShowHtml] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults([]);
    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, query })
      });
      if (!response.ok) throw new Error('Search failed');
      const data = await response.json();
      setResults(data);
      setShowHtml({});
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleHtml = idx => {
    setShowHtml(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)',
      padding: 0,
      margin: 0,
      fontFamily: 'Inter, sans-serif',
    }}>
      <header style={{
        textAlign: 'center',
        padding: '2rem 0 1rem 0',
        fontWeight: 700,
        fontSize: '2.5rem',
        letterSpacing: '-1px',
        color: '#3730a3',
      }}>
        Website Content Search
        <div style={{
          fontWeight: 400,
          fontSize: '1.1rem',
          color: '#6366f1',
          marginTop: 8
        }}>
          Search through website content with precision
        </div>
      </header>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
      }}>
        <form onSubmit={handleSubmit} style={{
          background: '#fff',
          borderRadius: 16,
          boxShadow: '0 4px 24px 0 rgba(55,48,163,0.08)',
          padding: '2rem 2.5rem',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 18,
          minWidth: 350,
          maxWidth: 420,
          width: '100%',
        }}>
          <input
            type="text"
            placeholder="https://example.com"
            value={url}
            onChange={e => setUrl(e.target.value)}
            required
            style={{
              width: '100%',
              padding: '0.8rem 1rem',
              borderRadius: 8,
              border: '1px solid #c7d2fe',
              fontSize: '1rem',
              outline: 'none',
              marginBottom: 4,
              background: '#f1f5f9',
              transition: 'border 0.2s',
            }}
          />
          <input
            type="text"
            placeholder="Search query"
            value={query}
            onChange={e => setQuery(e.target.value)}
            required
            style={{
              width: '100%',
              padding: '0.8rem 1rem',
              borderRadius: 8,
              border: '1px solid #c7d2fe',
              fontSize: '1rem',
              outline: 'none',
              background: '#f1f5f9',
              transition: 'border 0.2s',
            }}
          />
          <button type="submit" disabled={loading} style={{
            width: '100%',
            padding: '0.8rem',
            borderRadius: 8,
            border: 'none',
            background: 'linear-gradient(90deg, #6366f1 0%, #3730a3 100%)',
            color: '#fff',
            fontWeight: 600,
            fontSize: '1.1rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            boxShadow: '0 2px 8px 0 rgba(99,102,241,0.08)',
            transition: 'background 0.2s',
          }}>
            {loading ? 'Searching...' : 'Search'}
          </button>
          {error && <div style={{ color: '#dc2626', fontWeight: 500, marginTop: 8 }}>{error}</div>}
        </form>
        <div style={{ width: '100%', maxWidth: 700, margin: '2.5rem auto 0 auto' }}>
          {results.length > 0 && (
            <div style={{
              fontWeight: 600,
              fontSize: '1.2rem',
              color: '#3730a3',
              marginBottom: 18,
              textAlign: 'center',
            }}>
              Search Results
            </div>
          )}
          {results.map((result, idx) => (
            <div
              key={idx}
              style={{
                border: '1.5px solid #c7d2fe',
                borderRadius: 14,
                background: '#fff',
                boxShadow: '0 2px 12px 0 rgba(99,102,241,0.06)',
                padding: '1.2rem 1.5rem',
                marginBottom: 18,
                transition: 'box-shadow 0.2s',
                position: 'relative',
              }}
            >
              <div style={{
                position: 'absolute',
                top: 18,
                right: 18,
                background: '#e0e7ff',
                color: '#3730a3',
                borderRadius: 8,
                padding: '0.3rem 0.7rem',
                fontWeight: 600,
                fontSize: '0.95rem',
                boxShadow: '0 1px 4px 0 rgba(99,102,241,0.08)',
              }}>
                {(result.score * 100).toFixed(1)}% match
              </div>
              <div style={{ color: '#6366f1', fontWeight: 600, marginBottom: 6, fontSize: '1.05rem' }}>
                Path: <span style={{ color: '#3730a3', fontWeight: 500 }}>{result.path}</span>
              </div>
              <div style={{
                background: '#f1f5f9',
                borderRadius: 8,
                padding: '0.9rem 1rem',
                fontFamily: 'JetBrains Mono, monospace',
                fontSize: '1rem',
                color: '#334155',
                whiteSpace: 'pre-wrap',
                marginTop: 6,
                marginBottom: 2,
                lineHeight: 1.6,
                maxHeight: 220,
                overflowY: 'auto',
              }}>
                {result.chunk}
              </div>
              <div style={{ marginTop: 8 }}>
                <button
                  onClick={() => toggleHtml(idx)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#2563eb',
                    fontWeight: 600,
                    cursor: 'pointer',
                    fontSize: '1rem',
                    padding: 0,
                  }}
                >
                  {showHtml[idx] ? 'Hide HTML e' : 'View HTML  3e'}
                </button>
              </div>
              {showHtml[idx] && (
                <div style={{
                  background: '#f3f4f6',
                  borderRadius: 8,
                  padding: '0.9rem 1rem',
                  fontFamily: 'JetBrains Mono, monospace',
                  fontSize: '0.98rem',
                  color: '#334155',
                  whiteSpace: 'pre-wrap',
                  marginTop: 8,
                  marginBottom: 2,
                  lineHeight: 1.5,
                  maxHeight: 260,
                  overflowX: 'auto',
                  border: '1px solid #cbd5e1',
                }}>
                  {result.html}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
