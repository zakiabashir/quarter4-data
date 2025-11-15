'use client';

import React from 'react';
import Controls from './Controls';
import StackVisualizer from './StackVisualizer';
import InputTapeVisualizer from './InputTapeVisualizer';

import AnimatedStateGraph from './AnimatedStateGraph';

export default function Simulation() {
  return (
    <div className="flex flex-col gap-4 h-full">
      <h3 className="text-xl font-semibold">Controls</h3>
      <div className="p-2 border rounded-md bg-gray-50">
        <Controls />
      </div>

      <h3 className="text-xl font-semibold">Animated State Graph</h3>
      <div className="flex-grow p-4 border rounded-md bg-white shadow-sm flex items-center justify-center">
        <AnimatedStateGraph />
      </div>

      <h3 className="text-xl font-semibold">Stack Visualizer</h3>
      <div className="p-4 border rounded-md bg-white shadow-sm">
        <StackVisualizer />
      </div>

      <h3 className="text-xl font-semibold">Input Tape Visualizer</h3>
      <div className="p-4 border rounded-md bg-white shadow-sm">
        <InputTapeVisualizer />
      </div>
    </div>
  );
}
