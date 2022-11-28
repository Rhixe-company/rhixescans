"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _redux = require("redux");

var _userReducers = require("./userReducers");

var _comicsReducers = require("./comicsReducers");

var _chaptersReducers = require("./chaptersReducers");

var _default = (0, _redux.combineReducers)({
  comicsList: _comicsReducers.comicsListReducer,
  comicsDetails: _comicsReducers.comicsDetailsReducer,
  comicDelete: _comicsReducers.comicDeleteReducer,
  comicCreate: _comicsReducers.comicCreateReducer,
  comicUpdate: _comicsReducers.comicUpdateReducer,
  comicsTopRated: _comicsReducers.comicsTopRatedReducer,
  chaptersList: _chaptersReducers.chaptersListReducer,
  chaptersDetails: _chaptersReducers.chaptersDetailsReducer,
  chapterDelete: _chaptersReducers.chapterDeleteReducer,
  chapterCreate: _chaptersReducers.chapterCreateReducer,
  chapterUpdate: _chaptersReducers.chapterUpdateReducer,
  chaptersTopRatedReducer: _chaptersReducers.chaptersTopRatedReducer,
  userLogin: _userReducers.userLoginReducer,
  userRegister: _userReducers.userRegisterReducer,
  userDetails: _userReducers.userDetailsReducer,
  userUpdateProfile: _userReducers.userUpdateProfileReducer,
  userList: _userReducers.userListReducer,
  userDelete: _userReducers.userDeleteReducer,
  userUpdate: _userReducers.userUpdateReducer
});

exports["default"] = _default;