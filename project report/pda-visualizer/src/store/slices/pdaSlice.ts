import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { PDA, Transition } from '@/engine/pda';

const initialState: PDA = {
  states: ['q0', 'q1', 'q2'],
  inputAlphabet: ['a', 'b'],
  stackAlphabet: ['A', 'Z'],
  transitions: [],
  startState: 'q0',
  acceptStates: ['q2'],
};

const pdaSlice = createSlice({
  name: 'pda',
  initialState,
  reducers: {
    setPDA: (state, action: PayloadAction<PDA>) => {
      return action.payload;
    },
    addState: (state, action: PayloadAction<string>) => {
      if (!state.states.includes(action.payload)) {
        state.states.push(action.payload);
      }
    },
    addTransition: (state, action: PayloadAction<Transition>) => {
      state.transitions.push(action.payload);
    },
    addStackAlphabetSymbol: (state, action: PayloadAction<string>) => {
      if (!state.stackAlphabet.includes(action.payload)) {
        state.stackAlphabet.push(action.payload);
      }
    },
    addInputAlphabetSymbol: (state, action: PayloadAction<string>) => {
      if (!state.inputAlphabet.includes(action.payload)) {
        state.inputAlphabet.push(action.payload);
      }
    },
    toggleAcceptState: (state, action: PayloadAction<string>) => {
      const stateName = action.payload;
      if (state.acceptStates.includes(stateName)) {
        state.acceptStates = state.acceptStates.filter((s) => s !== stateName);
      } else {
        state.acceptStates.push(stateName);
      }
    },
  },

export const { setPDA, addState, addTransition, addStackAlphabetSymbol, toggleAcceptState, addInputAlphabetSymbol } = pdaSlice.actions;
export default pdaSlice.reducer;
