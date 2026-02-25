import React, { useState, useEffect, useRef } from 'react';
import { Send, Coffee, Heart, Star } from 'lucide-react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([{ role: 'bot', text: 'בניתי שלי, נשמה של סבתא. הכל מוכן ומחכה רק לך. מה נרשום היום?' }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  // שינוי שם הכרטיסייה למעלה
  useEffect(() => {
    document.title = "סבתא | זוכרת הכל!";
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input }),
      });
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'bot', text: data.reply }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', text: 'נשמה, נראה שיש תקלה בקווים... תנסי שוב.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="main-layout">
      <div className="chat-card">
        {/* Header */}
        <div className="chat-header">
          <div className="header-info">
            <div className="avatar">👵</div>
            <div>
              <h3>הבית של סבתא</h3>
              <small>מבשלת לך פתרונות...</small>
            </div>
          </div>
          <Heart className="heart-icon" fill="currentColor" />
        </div>

        {/* Messages */}
        <div className="messages-container">
          {messages.map((m, i) => (
            <div key={i} className={`msg-row ${m.role === 'user' ? 'user' : 'bot'}`}>
              <div className="msg-bubble">
                {m.text}
              </div>
            </div>
          ))}
          {isLoading && <div className="loading">סבתא כותבת...</div>}
          <div ref={scrollRef} />
        </div>

        {/* Input */}
        <div className="input-footer">
          <input 
            value={input} 
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="דברי איתי, נשמה..."
          />
          <button onClick={handleSend} className="send-btn">
            <Send size={20} style={{ transform: 'rotate(180deg)' }} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;