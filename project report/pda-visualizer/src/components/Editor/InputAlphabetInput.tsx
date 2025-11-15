'use client';

import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addInputAlphabetSymbol } from '@/store/slices/pdaSlice'; // Assuming this action exists
import { RootState } from '@/lib/store';

export default function InputAlphabetInput() {
  const dispatch = useDispatch();
  const inputAlphabet = useSelector((state: RootState) => state.pda.inputAlphabet);
  const [newSymbol, setNewSymbol] = useState('');

  const handleAddSymbol = () => {
    if (newSymbol && !inputAlphabet.includes(newSymbol)) {
      dispatch(addInputAlphabetSymbol(newSymbol));
      setNewSymbol('');
    }
  };

  return (
    <div>
      <div className="flex gap-2">
        <input
          type="text"
          value={newSymbol}
          onChange={(e) => setNewSymbol(e.target.value)}
          placeholder="New input symbol"
          className="p-2 border rounded-md w-full"
          maxLength={1} // Input symbols are typically single characters
        />
        <button onClick={handleAddSymbol} className="p-2 bg-blue-500 text-white rounded-md">
          Add Symbol
        </button>
      </div>
      <div className="mt-2 flex flex-wrap gap-2">
        {inputAlphabet.map((symbol) => (
          <div key={symbol} className="p-2 bg-gray-200 rounded-md text-sm">
            {symbol}
          </div>
        ))}
      </div>
    </div>
  );
}
