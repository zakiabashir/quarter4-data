import React, { useState, useEffect, useRef } from 'react';
import styles from './InteractiveCodeBlock.module.css';

const InteractiveCodeBlock = ({ children, language = 'python' }) => {
  const [code, setCode] = useState(children);
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [pyodideLoaded, setPyodideLoaded] = useState(false);
  const pyodideRef = useRef(null);

  useEffect(() => {
    loadPyodide();
  }, []);

  const loadPyodide = async () => {
    try {
      // Load Pyodide index
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js';
      script.async = true;

      script.onload = async () => {
        pyodideRef.current = await window.loadPyodide({
          indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/'
        });

        // Pre-load common packages
        await pyodideRef.current.loadPackage(['numpy', 'matplotlib', 'scipy']);
        setPyodideLoaded(true);
      };

      document.head.appendChild(script);
    } catch (error) {
      console.error('Failed to load Pyodide:', error);
      setOutput('Failed to load Python environment. Please refresh the page.');
    }
  };

  const runCode = async () => {
    if (!pyodideLoaded || !pyodideRef.current) {
      setOutput('Python environment is still loading. Please wait...');
      return;
    }

    setIsRunning(true);
    setOutput('');

    try {
      // Capture stdout
      pyodideRef.current.runPython(`
import sys
from io import StringIO
sys.stdout = StringIO()
      `);

      // Run the user's code
      pyodideRef.current.runPython(code);

      // Get the output
      const output = pyodideRef.current.runPython(`
output = sys.stdout.getvalue()
sys.stdout = sys.__stdout__
output
      `);

      setOutput(output || 'Code executed successfully (no output)');
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  const resetCode = () => {
    setCode(children);
    setOutput('');
  };

  if (language !== 'python') {
    // For non-Python code, just display as a regular code block
    return (
      <div className={styles.codeBlock}>
        <pre>
          <code className={`language-${language}`}>{children}</code>
        </pre>
      </div>
    );
  }

  return (
    <div className={styles.interactiveContainer}>
      <div className={styles.codeEditor}>
        <div className={styles.editorHeader}>
          <span>Python Code Editor</span>
          <div className={styles.editorButtons}>
            <button
              onClick={resetCode}
              className={styles.resetButton}
              disabled={isRunning}
            >
              Reset
            </button>
            <button
              onClick={runCode}
              className={styles.runButton}
              disabled={isRunning || !pyodideLoaded}
            >
              {isRunning ? 'Running...' : 'Run Code'}
            </button>
          </div>
        </div>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className={styles.codeTextarea}
          placeholder="Enter your Python code here..."
          disabled={isRunning}
        />
      </div>

      {output && (
        <div className={styles.outputContainer}>
          <div className={styles.outputHeader}>Output:</div>
          <pre className={styles.output}>{output}</pre>
        </div>
      )}

      {!pyodideLoaded && (
        <div className={styles.loadingIndicator}>
          Loading Python environment...
        </div>
      )}
    </div>
  );
};

export default InteractiveCodeBlock;