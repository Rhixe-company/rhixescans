import {
  COMICS_LIST_REQUEST,
  COMICS_LIST_SUCCESS,
  COMICS_LIST_FAIL,
  COMICS_DETAILS_REQUEST,
  COMICS_DETAILS_SUCCESS,
  COMICS_DETAILS_FAIL,
  COMICS_DELETE_REQUEST,
  COMICS_DELETE_SUCCESS,
  COMICS_DELETE_FAIL,
  COMICS_CREATE_REQUEST,
  COMICS_CREATE_SUCCESS,
  COMICS_CREATE_FAIL,
  COMICS_CREATE_RESET,
  COMICS_UPDATE_REQUEST,
  COMICS_UPDATE_SUCCESS,
  COMICS_UPDATE_FAIL,
  COMICS_UPDATE_RESET,
  COMICS_TOP_REQUEST,
  COMICS_TOP_SUCCESS,
  COMICS_TOP_FAIL,
} from "../constants/comicsConstants";

export const comicsListReducer = (state = { comics: [] }, action) => {
  switch (action.type) {
    case COMICS_LIST_REQUEST:
      return { loading: true, comics: [] };

    case COMICS_LIST_SUCCESS:
      return {
        loading: false,
        comics: action.payload.comics,
        comics_count: action.payload.comics_count,
        page: action.payload.page,
        pages: action.payload.pages,
      };

    case COMICS_LIST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const comicsDetailsReducer = (state = { comic: [] }, action) => {
  switch (action.type) {
    case COMICS_DETAILS_REQUEST:
      return { loading: true, ...state };

    case COMICS_DETAILS_SUCCESS:
      return { loading: false, comic: action.payload };

    case COMICS_DETAILS_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const comicDeleteReducer = (state = {}, action) => {
  switch (action.type) {
    case COMICS_DELETE_REQUEST:
      return { loading: true };

    case COMICS_DELETE_SUCCESS:
      return { loading: false, success: true };

    case COMICS_DELETE_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const comicCreateReducer = (state = {}, action) => {
  switch (action.type) {
    case COMICS_CREATE_REQUEST:
      return { loading: true };

    case COMICS_CREATE_SUCCESS:
      return { loading: false, success: true, comic: action.payload };

    case COMICS_CREATE_FAIL:
      return { loading: false, error: action.payload };

    case COMICS_CREATE_RESET:
      return {};

    default:
      return state;
  }
};

export const comicUpdateReducer = (state = { comic: {} }, action) => {
  switch (action.type) {
    case COMICS_UPDATE_REQUEST:
      return { loading: true };

    case COMICS_UPDATE_SUCCESS:
      return { loading: false, success: true, comic: action.payload };

    case COMICS_UPDATE_FAIL:
      return { loading: false, error: action.payload };

    case COMICS_UPDATE_RESET:
      return { comic: {} };

    default:
      return state;
  }
};

export const comicsTopRatedReducer = (state = { comics: [] }, action) => {
  switch (action.type) {
    case COMICS_TOP_REQUEST:
      return { loading: true, comics: [] };

    case COMICS_TOP_SUCCESS:
      return { loading: false, comics: action.payload };

    case COMICS_TOP_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};
