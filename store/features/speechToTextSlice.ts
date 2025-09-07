import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SpeechToTextState {
  text: string;
  loading: boolean;
  error: string | null;
}

const initialState: SpeechToTextState = {
  text: '',
  loading: false,
  error: null,
};

const speechToTextSlice = createSlice({
  name: 'speechToText',
  initialState,
  reducers: {
    setText(state, action: PayloadAction<string>) {
      state.text = action.payload;
      state.loading = false;
      state.error = null;
    },
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
      state.loading = false;
    },
    clearText(state) {
      state.text = '';
      state.error = null;
      state.loading = false;
    },
  },
});

export const { setText, setLoading, setError, clearText } = speechToTextSlice.actions;
export default speechToTextSlice.reducer;
