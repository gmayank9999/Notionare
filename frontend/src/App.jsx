import React, { useState } from 'react';
import { Bot, Search, Layout, MessageSquare, Terminal, Loader2, Sparkles, Activity } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './index.css';

const API_BASE = "http://localhost:8000/api";

function App() {
  const [activeTab, setActiveTab] = useState('tasks');
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAction = async () => {
    if (activeTab !== 'monitor' && !input.trim()) return;
    setLoading(true);
    setResult(null);

    let endpoint = "";
    let payload = {};

    switch (activeTab) {
      case 'tasks':
        endpoint = "/task";
        payload = { user_text: input };
        break;
      case 'research':
        endpoint = "/research";
        payload = { goal: input };
        break;
      case 'workspace':
        endpoint = "/workspace";
        payload = { idea: input };
        break;
      case 'chat':
        endpoint = "/chat";
        payload = { query: input };
        break;
      case 'monitor':
        endpoint = "/monitor";
        payload = {};
        break;
    }

    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: Object.keys(payload).length > 0 ? JSON.stringify(payload) : undefined
      });
      const data = await res.json();
      setResult(data.message || data.answer || "Success!");
    } catch (err) {
      setResult(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (newTab) => {
    setActiveTab(newTab);
    setInput('');
    setResult(null);
  };

  return (
    <div className="container" style={{ maxWidth: '800px', width: '100%' }}>
      <header style={{ textAlign: 'center', marginBottom: '3rem' }} className="animate-fade-in">
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '1rem', borderRadius: '50%', boxShadow: '0 0 20px rgba(255, 255, 255, 0.05)' }}>
            <Bot size={48} color="#f3f4f6" />
          </div>
        </div>
        <h1>Notionaire</h1>
        <p>Your Autonomous AI Command Center</p>
      </header>

      <main className="glass-panel animate-fade-in" style={{ animationDelay: '0.1s' }}>
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
          <TabButton active={activeTab === 'tasks'} onClick={() => handleTabChange('tasks')} icon={<Terminal size={18} />} label="Tasks" />
          <TabButton active={activeTab === 'research'} onClick={() => handleTabChange('research')} icon={<Search size={18} />} label="Research" />
          <TabButton active={activeTab === 'workspace'} onClick={() => handleTabChange('workspace')} icon={<Layout size={18} />} label="Workspace" />
          <TabButton active={activeTab === 'chat'} onClick={() => handleTabChange('chat')} icon={<MessageSquare size={18} />} label="Chat RAG" />
          <TabButton active={activeTab === 'monitor'} onClick={() => handleTabChange('monitor')} icon={<Activity size={18} />} label="Monitor" />
        </div>

        <div style={{ position: 'relative' }}>
          <input 
            type="text" 
            className="input-field" 
            placeholder={getPlaceholder(activeTab)} 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAction()}
            disabled={activeTab === 'monitor'}
            style={{ opacity: activeTab === 'monitor' ? 0.5 : 1 }}
          />
          <button 
            className="btn" 
            style={{ position: 'absolute', right: '8px', top: '8px', padding: '0.4rem 1rem' }}
            onClick={handleAction}
            disabled={loading || (activeTab !== 'monitor' && !input.trim())}
          >
            {loading ? <Loader2 className="loading-pulse" size={18} /> : <Sparkles size={18} />}
            {loading ? 'Processing' : 'Execute'}
          </button>
        </div>

        {result && (
          <div className="glass-panel animate-fade-in" style={{ marginTop: '2rem', background: 'rgba(255, 255, 255, 0.03)', borderColor: 'rgba(255, 255, 255, 0.1)' }}>
            <h3 style={{ color: '#e5e7eb', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 500 }}>
              <Bot size={20} color="#9ca3af" /> Response
            </h3>
            <div className="markdown-body">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{result}</ReactMarkdown>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function TabButton({ active, onClick, icon, label }) {
  return (
    <button 
      onClick={onClick}
      style={{
        background: active ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
        border: `1px solid ${active ? 'rgba(255, 255, 255, 0.2)' : 'rgba(255, 255, 255, 0.05)'}`,
        color: active ? '#f3f4f6' : '#9ca3af',
        padding: '0.6rem 1.2rem',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        fontWeight: 500,
        fontSize: '0.9rem'
      }}
    >
      {icon} {label}
    </button>
  );
}

function getPlaceholder(tab) {
  switch(tab) {
    case 'tasks': return "E.g., Complete math homework by Friday...";
    case 'research': return "E.g., Compare top 3 mechanical keyboards...";
    case 'workspace': return "E.g., Build a multiplayer chess game...";
    case 'chat': return "E.g., What were the key findings from my keyboard research?";
    case 'monitor': return "Click Execute to scan the workspace for conflicts...";
    default: return "";
  }
}

export default App;
