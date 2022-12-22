import {
  BOOKMARK_ADD_ITEM,
  BOOKMARK_REMOVE_ITEM,
} from "../constants/bookmarkConstants";

export const bookmarkReducers = (state = { bookmarkItems: [] }, action) => {
  switch (action.type) {
    case BOOKMARK_ADD_ITEM:
      const item = action.payload;
      const existItem = state.bookmarkItems.find((x) => x.comic !== item.comic);
      if (existItem) {
        return {
          ...state,
          bookmarkItems: state.bookmarkItems.map((x) =>
            x === existItem ? item : x
          ),
        };
      } else {
        return {
          ...state,
          bookmarkItems: [...state.bookmarkItems, item],
        };
      }
    case BOOKMARK_REMOVE_ITEM:
      return {
        ...state,
        bookmarkItems: state.bookmarkItems.filter(
          (x) => x.comic !== action.payload
        ),
      };

    default:
      return state;
  }
};

export default bookmarkReducers;
