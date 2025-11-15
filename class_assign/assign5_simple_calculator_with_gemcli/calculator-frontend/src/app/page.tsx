"use client";

import { useState } from 'react';

type Operator = '+' | '-' | '*' | '/' | '^';

export default function Home() {
  const [display, setDisplay] = useState('0');
  const [firstOperand, setFirstOperand] = useState<number | null>(null);
  const [operator, setOperator] = useState<Operator | null>(null);
  const [waitingForSecondOperand, setWaitingForSecondOperand] = useState(false);

  const inputDigit = (digit: string) => {
    if (waitingForSecondOperand) {
      setDisplay(digit);
      setWaitingForSecondOperand(false);
    } else {
      setDisplay(display === '0' ? digit : display + digit);
    }
  };

  const inputDecimal = () => {
    if (!display.includes('.')) {
      setDisplay(display + '.');
    }
  };

  const clearDisplay = () => {
    setDisplay('0');
    setFirstOperand(null);
    setOperator(null);
    setWaitingForSecondOperand(false);
  };

  const performOperation = (nextOperator: Operator) => {
    const inputValue = parseFloat(display);

    if (firstOperand === null) {
      setFirstOperand(inputValue);
    } else if (operator) {
      const result = calculate(firstOperand, inputValue, operator);
      setDisplay(String(result));
      setFirstOperand(result);
    }

    setWaitingForSecondOperand(true);
    setOperator(nextOperator);
  };
  
  const performUnaryOperation = (operation: 'sin' | 'cos' | 'tan' | 'log' | 'sqrt') => {
    const inputValue = parseFloat(display);
    let result = 0;

    try {
        switch (operation) {
            case 'sin':
                result = Math.sin(inputValue);
                break;
            case 'cos':
                result = Math.cos(inputValue);
                break;
            case 'tan':
                result = Math.tan(inputValue);
                break;
            case 'log':
                if (inputValue <= 0) throw new Error("Log of non-positive");
                result = Math.log(inputValue);
                break;
            case 'sqrt':
                if (inputValue < 0) throw new Error("Sqrt of negative");
                result = Math.sqrt(inputValue);
                break;
        }
        setDisplay(String(result));
        setFirstOperand(result);
        setWaitingForSecondOperand(true);
    } catch (error: any) {
        setDisplay(error.message);
        setFirstOperand(null);
        setOperator(null);
        setWaitingForSecondOperand(true);
    }
  };


  const calculate = (first: number, second: number, op: Operator): number => {
    switch (op) {
      case '+':
        return first + second;
      case '-':
        return first - second;
      case '*':
        return first * second;
      case '/':
        if (second === 0) {
            alert("Cannot divide by zero");
            return first;
        }
        return first / second;
      case '^':
        return Math.pow(first, second);
    }
  };

  const handleEquals = () => {
    const inputValue = parseFloat(display);
    if (operator && firstOperand !== null) {
      const result = calculate(firstOperand, inputValue, operator);
      setDisplay(String(result));
      setFirstOperand(null);
      setOperator(null);
      setWaitingForSecondOperand(false);
    }
  };

  const Button = ({ children, onClick, className = '' }: { children: React.ReactNode, onClick: () => void, className?: string }) => (
    <button onClick={onClick} className={`bg-gray-200 hover:bg-gray-300 text-black font-bold py-4 rounded-lg text-2xl transition duration-200 ${className}`}>
      {children}
    </button>
  );

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-900 p-4">
      <div className="w-full max-w-md mx-auto">
        <div className="bg-gray-800 text-white text-5xl text-right font-mono rounded-t-lg p-4 pr-6 break-all">
          {display}
        </div>
        <div className="grid grid-cols-5 gap-1 bg-gray-800 rounded-b-lg p-1">
          {/* Row 1 */}
          <Button onClick={() => performUnaryOperation('sin')}>sin</Button>
          <Button onClick={() => performUnaryOperation('cos')}>cos</Button>
          <Button onClick={() => performUnaryOperation('tan')}>tan</Button>
          <Button onClick={() => performUnaryOperation('log')}>log</Button>
          <Button onClick={() => performUnaryOperation('sqrt')}>√</Button>
          
          {/* Row 2 */}
          <Button onClick={() => inputDigit('7')}>7</Button>
          <Button onClick={() => inputDigit('8')}>8</Button>
          <Button onClick={() => inputDigit('9')}>9</Button>
          <Button onClick={() => performOperation('/')} className="bg-orange-500 hover:bg-orange-600 text-white">÷</Button>
          <Button onClick={() => performOperation('^')} className="bg-orange-500 hover:bg-orange-600 text-white">^</Button>

          {/* Row 3 */}
          <Button onClick={() => inputDigit('4')}>4</Button>
          <Button onClick={() => inputDigit('5')}>5</Button>
          <Button onClick={() => inputDigit('6')}>6</Button>
          <Button onClick={() => performOperation('*')} className="bg-orange-500 hover:bg-orange-600 text-white">×</Button>
          <Button onClick={clearDisplay} className="bg-red-500 hover:bg-red-600 text-white">C</Button>

          {/* Row 4 */}
          <Button onClick={() => inputDigit('1')}>1</Button>
          <Button onClick={() => inputDigit('2')}>2</Button>
          <Button onClick={() => inputDigit('3')}>3</Button>
          <Button onClick={() => performOperation('-')} className="bg-orange-500 hover:bg-orange-600 text-white">−</Button>
          <Button onClick={handleEquals} className="bg-green-500 hover:bg-green-600 text-white row-span-2">=</Button>

          {/* Row 5 */}
          <Button onClick={() => inputDigit('0')} className="col-span-2">0</Button>
          <Button onClick={inputDecimal}>.</Button>
          <Button onClick={() => performOperation('+')} className="bg-orange-500 hover:bg-orange-600 text-white">+</Button>
        </div>
      </div>
    </main>
  );
}