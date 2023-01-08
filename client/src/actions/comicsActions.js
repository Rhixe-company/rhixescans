import axios from "axios";
import {
  COMICS_LIST_REQUEST,
  COMICS_LIST_SUCCESS,
  COMICS_LIST_FAIL,
  COMICS_DETAILS_REQUEST,
  COMICS_DETAILS_SUCCESS,
  COMICS_DETAILS_FAIL,
} from "../constants/comicsConstants";

export const listComics =
  (keyword = "") =>
  async (dispatch) => {
    try {
      dispatch({ type: COMICS_LIST_REQUEST });

      const { data } = await axios.get(`/api/comics${keyword}`);

      dispatch({
        type: COMICS_LIST_SUCCESS,
        payload: data,
      });
    } catch (error) {
      dispatch({
        type: COMICS_LIST_FAIL,
        payload:
          error.response && error.response.data.detail
            ? error.response.data.detail
            : error.message,
      });
    }
  };

export const listComicDetails = (id) => async (dispatch) => {
  try {
    dispatch({ type: COMICS_DETAILS_REQUEST });

    const { data } = await axios.get(`/api/comics/${id}`);

    dispatch({
      type: COMICS_DETAILS_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: COMICS_DETAILS_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};
