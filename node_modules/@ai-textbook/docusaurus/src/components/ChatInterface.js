import React, { useState, useEffect, useRef } from 'react';
import styles from './ChatInterface.module.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { type: 'assistant', content: 'Hello! I\'m your AI assistant for the Physical AI textbook. How can I help you today?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { type: 'user', content: inputValue };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the chat API
      const response = await fetch('http://localhost:3001/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          context: 'physical_ai_textbook'
        }),
      });

      const data = await response.json();

      const assistantMessage = {
        type: 'assistant',
        content: data.response || 'I apologize, but I couldn\'t process your request. Please try again.'
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        type: 'assistant',
        content: 'Sorry, I\'m having trouble connecting right now. Please make sure the backend services are running.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const sampleQuestions = [
    'What is Physical AI?',
    'Explain the perception-action loop',
    'What sensors are used in robotics?',
    'How does LiDAR work?',
    'What are the challenges in Physical AI?'
  ];

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <h2>AI Assistant</h2>
        <p>Ask questions about Physical AI and robotics</p>
      </div>

      <div className={styles.messagesContainer}>
        {messages.map((message, index) => (
          <div
            key={index}
            className={`${styles.message} ${styles[message.type]}`}
          >
            <div className={styles.messageContent}>
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className={`${styles.message} ${styles.assistant}`}>
            <div className={styles.typingIndicator}>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputContainer}>
        <div className={styles.sampleQuestions}>
          <p>Try asking:</p>
          <div className={styles.questionTags}>
            {sampleQuestions.map((question, index) => (
              <button
                key={index}
                className={styles.questionTag}
                onClick={() => setInputValue(question)}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
        <div className={styles.inputWrapper}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question..."
            className={styles.messageInput}
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
            className={styles.sendButton}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;