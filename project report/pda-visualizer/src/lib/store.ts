import { configureStore } from '@reduxjs/toolkit'
import pdaReducer from '../store/slices/pdaSlice'
import simulationReducer from '../store/slices/simulationSlice'

export const makeStore = () => {
  return configureStore({
    reducer: {
      pda: pdaReducer,
      simulation: simulationReducer,
    },
  })
}

// Infer the type of makeStore
export type AppStore = ReturnType<typeof makeStore>
// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<AppStore['getState']>
export type AppDispatch = AppStore['dispatch']
