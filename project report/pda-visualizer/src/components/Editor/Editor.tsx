'use client';

import React from 'react';
import StateCreator from './StateCreator';
import InputAlphabetInput from './InputAlphabetInput'; // Import the new component
import StackAlphabetInput from './StackAlphabetInput';
import TransitionTable from './TransitionTable';
import AcceptStateSelector from './AcceptStateSelector';

export default function Editor() {
  return (
    <div className="flex flex-col gap-4">
      <h3 className="text-xl font-semibold">States</h3>
      <div className="p-2 border rounded-md bg-gray-50">
        <StateCreator />
      </div>

      <h3 className="text-xl font-semibold">Input Alphabet</h3> {/* New section for Input Alphabet */}
      <div className="p-2 border rounded-md bg-gray-50">
        <InputAlphabetInput />
      </div>

      <h3 className="text-xl font-semibold">Stack Alphabet</h3>
      <div className="p-2 border rounded-md bg-gray-50">
        <StackAlphabetInput />
      </div>

      <h3 className="text-xl font-semibold">Transitions</h3>
      <div className="p-2 border rounded-md bg-gray-50">
        <TransitionTable />
      </div>

      <h3 className="text-xl font-semibold">Accept States</h3>
      <div className="p-2 border rounded-md bg-gray-50">
        <AcceptStateSelector />
      </div>
    </div>
  );
}
