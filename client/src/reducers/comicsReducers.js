import {
  COMICS_LIST_REQUEST,
  COMICS_LIST_SUCCESS,
  COMICS_LIST_FAIL,
  COMICS_DETAILS_REQUEST,
  COMICS_DETAILS_SUCCESS,
  COMICS_DETAILS_FAIL,
} from "../constants/comicsConstants";

export const comicsListReducer = (state = {}, action) => {
  switch (action.type) {
    case COMICS_LIST_REQUEST:
      return { loading: true };

    case COMICS_LIST_SUCCESS:
      return {
        ...state,
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

export const comicDetailsReducer = (state = {}, action) => {
  switch (action.type) {
    case COMICS_DETAILS_REQUEST:
      return { loading: true };

    case COMICS_DETAILS_SUCCESS:
      return {
        ...state,
        loading: false,
        comic: action.payload.comic,
        chapters: action.payload.chapters,
      };

    case COMICS_DETAILS_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};
