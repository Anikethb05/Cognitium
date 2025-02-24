import { useState } from 'react';
import axios from 'axios';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState([]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');

    if (input.startsWith('@visual')) {
      setProgress(10);
      setLogs(['Initiating video generation...']);

      try {
        const response = await axios.post('/api/generate-video', { topic: input });
        const { video_url, logs: serverLogs, message } = response.data;

        setProgress(50);
        setLogs((prev) => [...prev, ...serverLogs]);

        const videoMessage = {
          sender: 'bot',
          text: message,
          video: `http://localhost:8000${video_url}`,
          logs: serverLogs,
        };
        setMessages((prev) => [...prev, videoMessage]);
        setProgress(100);
      } catch (error) {
        const errorMessage = { sender: 'bot', text: `Error: ${error.message}` };
        setMessages((prev) => [...prev, errorMessage]);
        setProgress(0);
      } finally {
        setLogs([]);
      }
    } else {
      const botMessage = { sender: 'bot', text: 'Please use @visual <topic> to generate a video.' };
      setMessages([...messages, botMessage]);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
            {msg.video && (
              <>
                <video controls src={msg.video} width="100%" />
                <details>
                  <summary>View Logs</summary>
                  <pre>{msg.logs.join('\n')}</pre>
                </details>
              </>
            )}
          </div>
        ))}
      </div>
      {progress > 0 && progress < 100 && (
        <div className="progress-bar">
          <div style={{ width: `${progress}%` }}></div>
        </div>
      )}
      {logs.length > 0 && (
        <div className="logs">
          <h3>Progress Logs</h3>
          <pre>{logs.join('\n')}</pre>
        </div>
      )}
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type @visual <topic> to generate a video..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}