import axios from "axios";
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
  COMICS_UPDATE_REQUEST,
  COMICS_UPDATE_SUCCESS,
  COMICS_UPDATE_FAIL,
  COMICS_TOP_REQUEST,
  COMICS_TOP_SUCCESS,
  COMICS_TOP_FAIL,
  GENRES_REQUEST,
  GENRES_SUCCESS,
  GENRES_FAIL,
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

export const listTopComics = () => async (dispatch, getState) => {
  try {
    dispatch({ type: COMICS_TOP_REQUEST });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.get(`/api/comics/top/`, config);

    dispatch({
      type: COMICS_TOP_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: COMICS_TOP_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const listComicsDetails = (id) => async (dispatch, getState) => {
  try {
    dispatch({ type: COMICS_DETAILS_REQUEST });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.get(`/api/comics/${id}`, config);

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

export const deleteComic = (id) => async (dispatch, getState) => {
  try {
    dispatch({
      type: COMICS_DELETE_REQUEST,
    });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.delete(`/api/comics/delete/${id}/`, config);
    console.log(data);
    dispatch({
      type: COMICS_DELETE_SUCCESS,
    });
  } catch (error) {
    dispatch({
      type: COMICS_DELETE_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const createComic = () => async (dispatch, getState) => {
  try {
    dispatch({
      type: COMICS_CREATE_REQUEST,
    });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.post(`/api/comics/create/`, {}, config);
    dispatch({
      type: COMICS_CREATE_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: COMICS_CREATE_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const updateComic = (comic) => async (dispatch, getState) => {
  try {
    dispatch({
      type: COMICS_UPDATE_REQUEST,
    });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.put(
      `/api/comics/update/${comic.id}/`,
      comic,
      config
    );
    dispatch({
      type: COMICS_UPDATE_SUCCESS,
      payload: data,
    });

    dispatch({
      type: COMICS_DETAILS_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: COMICS_UPDATE_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const listGenres = () => async (dispatch, getState) => {
  try {
    dispatch({ type: GENRES_REQUEST });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.get(`/api/comics/genres/`, config);

    dispatch({
      type: GENRES_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: GENRES_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};
