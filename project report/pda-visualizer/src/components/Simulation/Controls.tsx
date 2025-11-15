'use client';

import React, { useState, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { startSimulation, stopSimulation, setSimulationState } from '@/store/slices/simulationSlice';
import { RootState } from '@/lib/store';
import { PDAEngine } from '@/engine/pda';

export default function Controls() {
  const dispatch = useDispatch();
  const { isRunning, remainingInput, currentState, stack, isAccepted } = useSelector((state: RootState) => state.simulation);
  const pda = useSelector((state: RootState) => state.pda);

  const [inputString, setInputString] = useState('');
  const pdaEngineRef = useRef<PDAEngine | null>(null);

  const initializeEngine = (input: string) => {
    pdaEngineRef.current = new PDAEngine(pda, input);
    dispatch(setSimulationState(pdaEngineRef.current.getSimulationState()));
  };

  const handleStart = () => {
    if (inputString && pdaEngineRef.current) {
      dispatch(startSimulation(inputString));
      const { isAccepted: finalAccepted, history } = pdaEngineRef.current.simulate();
      // Update UI with the final state from the simulation history
      if (history.length > 0) {
        dispatch(setSimulationState({ ...history[history.length - 1], isAccepted: finalAccepted }));
      }
      dispatch(stopSimulation()); // Simulation is complete
    } else if (inputString) {
      initializeEngine(inputString);
      handleStart(); // Re-call start after initialization
    }
  };

  const handleStep = () => {
    if (pdaEngineRef.current) {
      const stepped = pdaEngineRef.current.step();
      if (stepped) {
        dispatch(setSimulationState(pdaEngineRef.current.getSimulationState()));
      } else {
        // No more steps possible, simulation halted
        dispatch(stopSimulation());
      }
    }
  };

  const handleReset = () => {
    dispatch(stopSimulation());
    dispatch(setSimulationState({
      currentState: pda.startState,
      stack: ['Z0'], // Reset to initial stack
      remainingInput: '',
      isAccepted: false,
      isRunning: false,
    }));
    setInputString('');
    pdaEngineRef.current = null; // Clear the engine instance
  };

  return (
    <div className="flex flex-col gap-2">
      <div className="flex gap-2">
        <input
          type="text"
          value={inputString}
          onChange={(e) => setInputString(e.target.value)}
          placeholder="Enter input string"
          className="p-2 border rounded-md w-full"
          disabled={isRunning}
        />
        <button onClick={() => initializeEngine(inputString)} className="p-2 bg-gray-400 text-white rounded-md" disabled={isRunning || !inputString || pdaEngineRef.current !== null}>
          Init
        </button>
        <button onClick={handleStart} className="p-2 bg-green-500 text-white rounded-md" disabled={isRunning || !pdaEngineRef.current}>
          Play
        </button>
        <button onClick={handleStep} className="p-2 bg-blue-500 text-white rounded-md" disabled={isRunning || !pdaEngineRef.current}>
          Step
        </button>
        <button onClick={handleReset} className="p-2 bg-gray-500 text-white rounded-md">
          Reset
        </button>
      </div>
      {isRunning && <p className="text-sm text-gray-600">Running simulation with input: {remainingInput}</p>}
      {!isRunning && pdaEngineRef.current && (
        <p className="text-sm text-gray-600">
          Simulation finished. Accepted: {isAccepted ? 'Yes' : 'No'}. Current State: {currentState}. Stack: [{stack.join(', ')}]
        </p>
      )}
    </div>
  );
}
