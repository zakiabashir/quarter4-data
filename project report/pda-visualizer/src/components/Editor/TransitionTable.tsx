'use client';

import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addTransition } from '@/store/slices/pdaSlice';
import { RootState } from '@/lib/store';
import { Transition } from '@/engine/pda';

export default function TransitionTable() {
  const dispatch = useDispatch();
  const { states, inputAlphabet, stackAlphabet, transitions } = useSelector((state: RootState) => state.pda);

  const [fromState, setFromState] = useState('');
  const [input, setInput] = useState('');
  const [stackTop, setStackTop] = useState('');
  const [toState, setToState] = useState('');
  const [pushSymbol, setPushSymbol] = useState('');

  const handleAddTransition = () => {
    if (fromState && input && stackTop && toState && pushSymbol) {
      const newTransition: Transition = {
        fromState,
        input,
        stackTop,
        toState,
        pushSymbol,
      };
      dispatch(addTransition(newTransition));
      // Clear form
      setFromState('');
      setInput('');
      setStackTop('');
      setToState('');
      setPushSymbol('');
    }
  };

  return (
    <div>
      <div className="grid grid-cols-5 gap-2 mb-4">
        <select
          value={fromState}
          onChange={(e) => setFromState(e.target.value)}
          className="p-2 border rounded-md"
        >
          <option value="">From State</option>
          {states.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Input (ε for empty)"
          className="p-2 border rounded-md"
        />
        <input
          type="text"
          value={stackTop}
          onChange={(e) => setStackTop(e.target.value)}
          placeholder="Stack Top (ε for empty)"
          className="p-2 border rounded-md"
        />
        <select
          value={toState}
          onChange={(e) => setToState(e.target.value)}
          className="p-2 border rounded-md"
        >
          <option value="">To State</option>
          {states.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <input
          type="text"
          value={pushSymbol}
          onChange={(e) => setPushSymbol(e.target.value)}
          placeholder="Push Symbol (ε for empty)"
          className="p-2 border rounded-md"
        />
      </div>
      <button onClick={handleAddTransition} className="p-2 bg-blue-500 text-white rounded-md w-full">
        Add Transition
      </button>

      <div className="mt-4">
        <h4 className="text-lg font-medium mb-2">Current Transitions:</h4>
        {transitions.length === 0 ? (
          <p className="text-gray-500">No transitions defined yet.</p>
        ) : (
          <ul className="border rounded-md p-2 bg-white">
            {transitions.map((t, index) => (
              <li key={index} className="text-sm border-b last:border-b-0 p-1">
                ({t.fromState}, {t.input}, {t.stackTop}) → ({t.toState}, {t.pushSymbol})
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
