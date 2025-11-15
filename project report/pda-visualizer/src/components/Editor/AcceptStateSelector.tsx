'use client';

import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toggleAcceptState } from '@/store/slices/pdaSlice'; // Assuming this action exists
import { RootState } from '@/lib/store';

export default function AcceptStateSelector() {
  const dispatch = useDispatch();
  const { states, acceptStates } = useSelector((state: RootState) => state.pda);

  const handleToggleAcceptState = (stateName: string) => {
    dispatch(toggleAcceptState(stateName));
  };

  return (
    <div className="flex flex-wrap gap-2">
      {states.map((state) => (
        <label key={state} className="flex items-center p-2 bg-gray-200 rounded-md text-sm cursor-pointer">
          <input
            type="checkbox"
            checked={acceptStates.includes(state)}
            onChange={() => handleToggleAcceptState(state)}
            className="mr-1"
          />
          {state}
        </label>
      ))}
    </div>
  );
}
