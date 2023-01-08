import {
  CHAPTERS_LIST_REQUEST,
  CHAPTERS_LIST_SUCCESS,
  CHAPTERS_LIST_FAIL,
  CHAPTERS_DETAILS_REQUEST,
  CHAPTERS_DETAILS_SUCCESS,
  CHAPTERS_DETAILS_FAIL,
} from "../constants/chaptersConstants";

export const chaptersListReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_LIST_REQUEST:
      return { loading: true };

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

export const chapterDetailsReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_DETAILS_REQUEST:
      return { loading: true };

    case CHAPTERS_DETAILS_SUCCESS:
      return {
        ...state,
        loading: false,
        chapter: action.payload.chapter,
        comic: action.payload.comic,
        chapters: action.payload.chapters,
      };

    case CHAPTERS_DETAILS_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};
