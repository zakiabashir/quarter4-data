'use client';

import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addState } from '@/store/slices/pdaSlice';
import { RootState } from '@/lib/store';

export default function StateCreator() {
  const dispatch = useDispatch();
  const { states, startState, acceptStates } = useSelector((state: RootState) => state.pda);
  const [newState, setNewState] = useState('');

  const handleAddState = () => {
    if (newState && !states.includes(newState)) {
      dispatch(addState(newState));
      setNewState('');
    }
  };

  return (
    <div>
      <div className="flex gap-2">
        <input
          type="text"
          value={newState}
          onChange={(e) => setNewState(e.target.value)}
          placeholder="New state name"
          className="p-2 border rounded-md w-full"
        />
        <button onClick={handleAddState} className="p-2 bg-blue-500 text-white rounded-md">
          Add State
        </button>
      </div>
      <div className="mt-2 flex flex-wrap gap-2">
        {states.map((state) => (
          <div key={state} className="p-2 bg-gray-200 rounded-md text-sm">
            {state}
            {state === startState && <span className="ml-1 text-green-500">(Start)</span>}
            {acceptStates.includes(state) && <span className="ml-1 text-blue-500">(Accept)</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
