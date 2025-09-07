import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './features/counterSlice';
import speechToTextReducer from './features/speechToTextSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    speechToText: speechToTextReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;