import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SimulationState {
  currentState: string;
  stack: string[];
  remainingInput: string;
  isAccepted: boolean;
  isRunning: boolean;
}

const initialState: SimulationState = {
  currentState: 'q0',
  stack: [],
  remainingInput: '',
  isAccepted: false,
  isRunning: false,
};

const simulationSlice = createSlice({
  name: 'simulation',
  initialState,
  reducers: {
    setSimulationState: (state, action: PayloadAction<Partial<SimulationState>>) => {
      Object.assign(state, action.payload);
    },
    startSimulation: (state, action: PayloadAction<string>) => {
      state.isRunning = true;
      state.remainingInput = action.payload;
      state.stack = [];
      state.isAccepted = false;
    },
    stopSimulation: (state) => {
      state.isRunning = false;
    },
    // Add other reducers for simulation steps
  },
});

export const { setSimulationState, startSimulation, stopSimulation } = simulationSlice.actions;
export default simulationSlice.reducer;
