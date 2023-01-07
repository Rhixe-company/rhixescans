import { combineReducers } from "redux";
import {
  userLoginReducer,
  userRegisterReducer,
  userDetailsReducer,
  userUpdateProfileReducer,
  userListReducer,
  userDeleteReducer,
  userUpdateReducer,
} from "./userReducers";
import { bookmarkReducers } from "./bookmarkReducers";

import {
  comicsLoadReducer,
  comicsListReducer,
  comicsDetailsReducer,
  comicDeleteReducer,
  comicCreateReducer,
  comicUpdateReducer,
  comicsTopRatedReducer,
  GenresListReducer,
} from "./comicsReducers";

import {
  chaptersListReducer,
  chaptersDetailsReducer,
  chapterDeleteReducer,
  chapterCreateReducer,
  chapterUpdateReducer,
  chaptersTopRatedReducer,
} from "./chaptersReducers";

const reducer = combineReducers({
  bookmark: bookmarkReducers,
  comicsLoad: comicsLoadReducer,
  comicsList: comicsListReducer,
  comicsDetails: comicsDetailsReducer,
  genresList: GenresListReducer,
  comicDelete: comicDeleteReducer,
  comicCreate: comicCreateReducer,
  comicUpdate: comicUpdateReducer,
  comicsTopRated: comicsTopRatedReducer,

  chaptersList: chaptersListReducer,
  chaptersDetails: chaptersDetailsReducer,
  chapterDelete: chapterDeleteReducer,
  chapterCreate: chapterCreateReducer,
  chapterUpdate: chapterUpdateReducer,
  chaptersTopRatedReducer: chaptersTopRatedReducer,

  userLogin: userLoginReducer,
  userRegister: userRegisterReducer,
  userDetails: userDetailsReducer,
  userUpdateProfile: userUpdateProfileReducer,
  userList: userListReducer,
  userDelete: userDeleteReducer,
  userUpdate: userUpdateReducer,
});

export default reducer;
