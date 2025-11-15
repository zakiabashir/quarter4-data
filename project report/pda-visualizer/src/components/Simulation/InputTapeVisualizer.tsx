'use client';

import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/lib/store';

export default function InputTapeVisualizer() {
  const { remainingInput } = useSelector((state: RootState) => state.simulation);

  // For simplicity, we'll just show the remaining input.
  // A more advanced visualizer would show the consumed part and highlight the current symbol.
  return (
    <div className="border rounded-md p-4 bg-white overflow-x-auto">
      <p className="text-gray-500 text-sm">Remaining Input:</p>
      <div className="flex gap-1 mt-2">
        {remainingInput.split('').map((char, index) => (
          <span
            key={index}
            className={`px-2 py-1 border rounded-md ${
              index === 0 ? 'bg-yellow-200 font-bold' : 'bg-gray-100'
            }`}
          >
            {char}
          </span>
        ))}
        {remainingInput.length === 0 && (
          <span className="px-2 py-1 text-gray-400">End of input</span>
        )}
      </div>
    </div>
  );
}
