import { combineReducers } from "redux";
import { chaptersListReducer, chapterDetailsReducer } from "./chaptersReducers";
import { comicsListReducer, comicDetailsReducer } from "./comicsReducers";
const reducer = combineReducers({
  comics: comicsListReducer,
  comic: comicDetailsReducer,
  chapters: chaptersListReducer,
  chapter: chapterDetailsReducer,
});

export default reducer;
