// This file will contain the core PDA simulation logic.

// Define the structure of a PDA
export interface PDA {
  states: string[];
  inputAlphabet: string[];
  stackAlphabet: string[];
  transitions: Transition[];
  startState: string;
  acceptStates: string[];
}

// Define the structure of a transition
export interface Transition {
  fromState: string;
  input: string;
  stackTop: string;
  toState: string;
  pushSymbol: string;
}

// The PDAEngine class will handle the simulation logic
export class PDAEngine {
  private pda: PDA;
  private currentState: string;
  private stack: string[];
  private input: string[];
  private inputIndex: number; // To keep track of the current input symbol

  constructor(pda: PDA, input: string) {
    this.pda = pda;
    this.currentState = pda.startState;
    this.stack = ['Z0']; // Initial stack symbol
    this.input = input.split('');
    this.inputIndex = 0;
  }

  // Helper for stack operations
  private push(symbol: string) {
    if (symbol !== 'ε') {
      this.stack.push(symbol);
    }
  }

  private pop(): string | undefined {
    return this.stack.pop();
  }

  private peek(): string | undefined {
    return this.stack[this.stack.length - 1];
  }

  // Executes a single step of the simulation
  step(): boolean {
    const currentInputSymbol = this.input[this.inputIndex] || 'ε'; // 'ε' for empty input
    const currentStackTop = this.peek() || 'ε'; // 'ε' for empty stack

    // Find all applicable transitions
    const applicableTransitions = this.pda.transitions.filter(t =>
      t.fromState === this.currentState &&
      (t.input === currentInputSymbol || t.input === 'ε') &&
      (t.stackTop === currentStackTop || t.stackTop === 'ε')
    );

    if (applicableTransitions.length === 0) {
      return false; // No valid transition, PDA halts
    }

    // For simplicity, pick the first applicable transition.
    // A full non-deterministic PDA would explore all paths.
    const chosenTransition = applicableTransitions[0];

    // Apply the transition
    this.currentState = chosenTransition.toState;

    // Pop from stack if stackTop is not epsilon
    if (chosenTransition.stackTop !== 'ε') {
      this.pop();
    }

    // Push to stack if pushSymbol is not epsilon
    if (chosenTransition.pushSymbol !== 'ε') {
      this.push(chosenTransition.pushSymbol);
    }

    // Advance input if input is not epsilon
    if (chosenTransition.input !== 'ε') {
      this.inputIndex++;
    }

    return true; // Transition successfully applied
  }

  // Simulates the entire input string
  simulate(): { isAccepted: boolean; history: any[] } {
    const history: any[] = [];
    history.push(this.getSimulationState());

    while (this.step()) {
      history.push(this.getSimulationState());
      // Check for infinite loops with epsilon transitions
      if (this.inputIndex >= this.input.length && this.input[this.inputIndex] === 'ε') {
        // If only epsilon transitions are left and state is not changing, break
        const lastTwoStates = history.slice(-2).map(s => s.currentState);
        if (lastTwoStates[0] === lastTwoStates[1]) {
          break;
        }
      }
      if (this.inputIndex > this.input.length + 100) { // Prevent infinite loops
        console.warn("Simulation likely in an infinite loop, stopping.");
        break;
      }
    }

    const isAccepted = this.pda.acceptStates.includes(this.currentState) && this.inputIndex === this.input.length && this.stack.length === 0;
    return { isAccepted, history };
  }

  // Returns the current state of the simulation
  getSimulationState() {
    return {
      currentState: this.currentState,
      stack: [...this.stack],
      remainingInput: this.input.slice(this.inputIndex).join(''),
      isAccepted: this.pda.acceptStates.includes(this.currentState) && this.inputIndex === this.input.length && this.stack.length === 0,
    };
  }
}
