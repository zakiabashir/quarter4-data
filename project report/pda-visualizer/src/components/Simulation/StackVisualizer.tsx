'use client';

import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/lib/store';

export default function StackVisualizer() {
  const stack = useSelector((state: RootState) => state.simulation.stack);

  return (
    <div className="flex flex-col-reverse items-center border rounded-md p-2 bg-white h-48 overflow-y-auto">
      {stack.length === 0 ? (
        <p className="text-gray-400 text-sm">Stack is empty</p>
      ) : (
        stack.map((symbol, index) => (
          <div
            key={index}
            className="w-10 h-8 bg-blue-200 border border-blue-400 flex items-center justify-center text-sm font-semibold mb-1"
          >
            {symbol}
          </div>
        ))
      )}
    </div>
  );
}
