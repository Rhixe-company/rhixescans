import { createStore, combineReducers, applyMiddleware } from "redux";
import { composeWithDevTools } from "redux-devtools-extension";
import thunk from "redux-thunk";
import {
  userLoginReducer,
  userRegisterReducer,
  userDetailsReducer,
  userUpdateProfileReducer,
  userListReducer,
  userDeleteReducer,
  userUpdateReducer,
} from "./reducers/userReducers";

import {
  comicsListReducer,
  comicsDetailsReducer,
  comicDeleteReducer,
  comicCreateReducer,
  comicUpdateReducer,
  comicsTopRatedReducer,
} from "./reducers/comicsReducers";

import {
  chaptersListReducer,
  chaptersDetailsReducer,
  chapterDeleteReducer,
  chapterCreateReducer,
  chapterUpdateReducer,
  chaptersTopRatedReducer,
} from "./reducers/chaptersReducers";

const reducer = combineReducers({
  comicsList: comicsListReducer,
  comicsDetails: comicsDetailsReducer,

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

const userInfoFromStorage = localStorage.getItem("userInfo")
  ? JSON.parse(localStorage.getItem("userInfo"))
  : null;

const initialState = {
  userLogin: { userInfo: userInfoFromStorage },
};

const middleware = [thunk];

const store = createStore(
  reducer,
  initialState,
  composeWithDevTools(applyMiddleware(...middleware))
);

export default store;
