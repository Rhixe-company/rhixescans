import axios from "axios";
import {
  BOOKMARK_ADD_ITEM,
  BOOKMARK_REMOVE_ITEM,
} from "../constants/bookmarkConstants";

export const addToBookmark = (id) => async (dispatch, getState) => {
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
    type: BOOKMARK_ADD_ITEM,
    payload: data.comic,
  });
  localStorage.setItem(
    "bookmarkItems",
    JSON.stringify(getState().cart.bookmarkItems)
  );
};

export const removeFromBookmark = (id) => (dispatch, getState) => {
  dispatch({
    type: BOOKMARK_REMOVE_ITEM,
    payload: id,
  });
  localStorage.setItem(
    "bookmarkItems",
    JSON.stringify(getState().cart.bookmarkItems)
  );
};
