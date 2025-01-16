import React, { useState } from 'react';
import { getAnswer } from '../services/api'; // Import the API service
import './ChatInterface.css';
import { IoCopy } from "react-icons/io5";

const ChatInterface = () => {
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);

    const handleMessageSubmit = async () => {
        try {
            // Add user question to chat history
            setChatHistory([...chatHistory, { sender: 'user', message }]);
            setMessage('');

            // Call the backend API
            const answer = await getAnswer(message);

            // Add bot response to chat history
            setChatHistory([...chatHistory, { sender: 'user', message }, { sender: 'bot', message: answer }]);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    const handleCopy = (text) => {
        navigator.clipboard.writeText(text)
            .then(() => alert('Copied to clipboard!'))
            .catch((err) => console.error('Error copying text:', err));
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>🍳 TasteNova</h1>
                <p>Your Intelligent Cooking Guide</p>
            </div>
            <div className="chat-window">
                {chatHistory.map((entry, index) => (
                    <div key={index} className={`chat-message ${entry.sender}`}>
                        <div className="avatar">
                            {entry.sender === 'user' ? '🙋‍♂️' : '🧑‍🍳'}
                        </div>
                        <div className="message-text">
                            <p>{entry.message}</p>
                        </div>
                        <button
                                className="copy-icon"
                                onClick={() => handleCopy(entry.message)}
                                title="Copy to clipboard"
                            >
                                <IoCopy />
                                {/* 📋 */}
                            </button>
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Ask a question..."
                />
                <button onClick={handleMessageSubmit}>Send</button>
            </div>
        </div>
    );
};

export default ChatInterface;
