import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import comicService from "./comicService";
const initialState = {
  comics: [],
  page: [],
  pages: [],
  count: [],
  isError: false,
  isSucess: false,
  isLoading: false,
  message: "",
};

// Create new Comic
export const createComic = createAsyncThunk(
  "comics/create",
  async (comicData, thunkAPI) => {
    try {
      const token = thunkAPI.getState().userLogin.userInfo.token;
      return await comicService.createComic(comicData, token);
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

// Get comics
export const getComics = createAsyncThunk(
  "comics/getAll",
  async (_, thunkAPI) => {
    try {
      const token = thunkAPI.getState().userLogin.userInfo.token;
      return await comicService.getComics(token);
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

// Delete Comic
export const deleteComic = createAsyncThunk(
  "comics/delete",
  async (id, thunkAPI) => {
    try {
      const token = thunkAPI.getState().userLogin.userInfo.token;
      return await comicService.deleteComic(id, token);
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

export const comicSlice = createSlice({
  name: "comic",
  initialState,
  reducers: {
    reset: (state) => initialState,
  },
  extraReducers: (builder) => {
    builder
      .addCase(createComic.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(createComic.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSucess = true;
        state.comics.push(action.payload);
      })
      .addCase(createComic.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })
      .addCase(getComics.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getComics.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSucess = true;
        state.comics = action.payload.comics;
        state.count = action.payload.comics_count;
        state.page = action.payload.page;
        state.pages = action.payload.pages;
      })
      .addCase(getComics.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })
      .addCase(deleteComic.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(deleteComic.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSucess = true;
        state.comics = state.comics.filter(
          (comic) => comic.id !== action.payload.id
        );
      })
      .addCase(deleteComic.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      });
  },
});

export const { reset } = comicSlice.actions;
export default comicSlice.reducer;
