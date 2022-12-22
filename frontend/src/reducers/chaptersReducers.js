import {
  CHAPTERS_LIST_REQUEST,
  CHAPTERS_LIST_SUCCESS,
  CHAPTERS_LIST_FAIL,
  CHAPTERS_DETAILS_REQUEST,
  CHAPTERS_DETAILS_SUCCESS,
  CHAPTERS_DETAILS_FAIL,
  CHAPTERS_DETAILS_RESET,
  CHAPTERS_DELETE_REQUEST,
  CHAPTERS_DELETE_SUCCESS,
  CHAPTERS_DELETE_FAIL,
  CHAPTERS_CREATE_REQUEST,
  CHAPTERS_CREATE_SUCCESS,
  CHAPTERS_CREATE_FAIL,
  CHAPTERS_CREATE_RESET,
  CHAPTERS_UPDATE_REQUEST,
  CHAPTERS_UPDATE_SUCCESS,
  CHAPTERS_UPDATE_FAIL,
  CHAPTERS_UPDATE_RESET,
  CHAPTERS_TOP_REQUEST,
  CHAPTERS_TOP_SUCCESS,
  CHAPTERS_TOP_FAIL,
} from "../constants/chaptersConstants";

const initialState = {
  chapters: [],
  chapter: {},
};

export const chaptersListReducer = (state = initialState, action) => {
  switch (action.type) {
    case CHAPTERS_LIST_REQUEST:
      return { ...state, loading: true, chapters: [] };

    case CHAPTERS_LIST_SUCCESS:
      return {
        ...state,
        loading: false,
        chapters: action.payload.chapters,
        chapters_count: action.payload.chapters_count,
        page: action.payload.page,
        pages: action.payload.pages,
      };

    case CHAPTERS_LIST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const chaptersDetailsReducer = (state = initialState, action) => {
  switch (action.type) {
    case CHAPTERS_DETAILS_REQUEST:
      return { ...state, loading: true, ...state };

    case CHAPTERS_DETAILS_SUCCESS:
      return {
        ...state,
        loading: false,
        chapter: action.payload.chapter,
        comic: action.payload.comic,
      };

    case CHAPTERS_DETAILS_FAIL:
      return { loading: false, error: action.payload };

    case CHAPTERS_DETAILS_RESET:
      return { chapter: {}, comic: {} };

    default:
      return state;
  }
};

export const chapterDeleteReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_DELETE_REQUEST:
      return { loading: true };

    case CHAPTERS_DELETE_SUCCESS:
      return { loading: false, success: true };

    case CHAPTERS_DELETE_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const chapterCreateReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_CREATE_REQUEST:
      return { loading: true };

    case CHAPTERS_CREATE_SUCCESS:
      return { loading: false, success: true, chapter: action.payload };

    case CHAPTERS_CREATE_FAIL:
      return { loading: false, error: action.payload };

    case CHAPTERS_CREATE_RESET:
      return {};

    default:
      return state;
  }
};

export const chapterUpdateReducer = (state = { chapter: {} }, action) => {
  switch (action.type) {
    case CHAPTERS_UPDATE_REQUEST:
      return { loading: true };

    case CHAPTERS_UPDATE_SUCCESS:
      return { loading: false, success: true, chapter: action.payload };

    case CHAPTERS_UPDATE_FAIL:
      return { loading: false, error: action.payload };

    case CHAPTERS_UPDATE_RESET:
      return { chapter: {} };

    default:
      return state;
  }
};

export const chaptersTopRatedReducer = (state = initialState, action) => {
  switch (action.type) {
    case CHAPTERS_TOP_REQUEST:
      return { loading: true, chapters: [] };

    case CHAPTERS_TOP_SUCCESS:
      return { loading: false, chapters: action.payload };

    case CHAPTERS_TOP_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};
