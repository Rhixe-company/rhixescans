import axios from "axios";
import {
  CHAPTERS_LIST_REQUEST,
  CHAPTERS_LIST_SUCCESS,
  CHAPTERS_LIST_FAIL,
  CHAPTERS_DETAILS_REQUEST,
  CHAPTERS_DETAILS_SUCCESS,
  CHAPTERS_DETAILS_FAIL,
} from "../constants/chaptersConstants";

export const listChapters = () => async (dispatch) => {
  try {
    dispatch({ type: CHAPTERS_LIST_REQUEST });

    const { data } = await axios.get(`/api/chapters/`);

    dispatch({
      type: CHAPTERS_LIST_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: CHAPTERS_LIST_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const listChapterDetails = (id) => async (dispatch) => {
  try {
    dispatch({ type: CHAPTERS_DETAILS_REQUEST });
    const { data } = await axios.get(`/api/chapters/${id}/`);

    dispatch({
      type: CHAPTERS_DETAILS_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: CHAPTERS_DETAILS_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};
