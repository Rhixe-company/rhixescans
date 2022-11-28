"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.comicsTopRatedReducer = exports.comicUpdateReducer = exports.comicCreateReducer = exports.comicDeleteReducer = exports.comicsDetailsReducer = exports.comicsListReducer = void 0;

var _comicsConstants = require("../constants/comicsConstants");

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(source, true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(source).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var comicsListReducer = function comicsListReducer() {
  var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {
    comics: []
  };
  var action = arguments.length > 1 ? arguments[1] : undefined;

  switch (action.type) {
    case _comicsConstants.COMICS_LIST_REQUEST:
      return {
        loading: true,
        comics: []
      };

    case _comicsConstants.COMICS_LIST_SUCCESS:
      return {
        loading: false,
        comics: action.payload.comics,
        page: action.payload.page,
        pages: action.payload.pages
      };

    case _comicsConstants.COMICS_LIST_FAIL:
      return {
        loading: false,
        error: action.payload
      };

    default:
      return state;
  }
};

exports.comicsListReducer = comicsListReducer;

var comicsDetailsReducer = function comicsDetailsReducer() {
  var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {
    comic: []
  };
  var action = arguments.length > 1 ? arguments[1] : undefined;

  switch (action.type) {
    case _comicsConstants.COMICS_DETAILS_REQUEST:
      return _objectSpread({
        loading: true
      }, state);

    case _comicsConstants.COMICS_DETAILS_SUCCESS:
      return {
        loading: false,
        comic: action.payload
      };

    case _comicsConstants.COMICS_DETAILS_FAIL:
      return {
        loading: false,
        error: action.payload
      };

    default:
      return state;
  }
};

exports.comicsDetailsReducer = comicsDetailsReducer;

var comicDeleteReducer = function comicDeleteReducer() {
  var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  var action = arguments.length > 1 ? arguments[1] : undefined;

  switch (action.type) {
    case _comicsConstants.COMICS_DELETE_REQUEST:
      return {
        loading: true
      };

    case _comicsConstants.COMICS_DELETE_SUCCESS:
      return {
        loading: false,
        success: true
      };

    case _comicsConstants.COMICS_DELETE_FAIL:
      return {
        loading: false,
        error: action.payload
      };

    default:
      return state;
  }
};

exports.comicDeleteReducer = comicDeleteReducer;

var comicCreateReducer = function comicCreateReducer() {
  var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  var action = arguments.length > 1 ? arguments[1] : undefined;

  switch (action.type) {
    case _comicsConstants.COMICS_CREATE_REQUEST:
      return {
        loading: true
      };

    case _comicsConstants.COMICS_CREATE_SUCCESS:
      return {
        loading: false,
        success: true,
        comic: action.payload
      };

    case _comicsConstants.COMICS_CREATE_FAIL:
      return {
        loading: false,
        error: action.payload
      };

    case _comicsConstants.COMICS_CREATE_RESET:
      return {};

    default:
      return state;
  }
};

exports.comicCreateReducer = comicCreateReducer;

var comicUpdateReducer = function comicUpdateReducer() {
  var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {
    comic: {}
  };
  var action = arguments.length > 1 ? arguments[1] : undefined;

  switch (action.type) {
    case _comicsConstants.COMICS_UPDATE_REQUEST:
      return {
        loading: true
      };

    case _comicsConstants.COMICS_UPDATE_SUCCESS:
      return {
        loading: false,
        success: true,
        comic: action.payload
      };

    case _comicsConstants.COMICS_UPDATE_FAIL:
      return {
        loading: false,
        error: action.payload
      };

    case _comicsConstants.COMICS_UPDATE_RESET:
      return {
        comic: {}
      };

    default:
      return state;
  }
};

exports.comicUpdateReducer = comicUpdateReducer;

var comicsTopRatedReducer = function comicsTopRatedReducer() {
  var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {
    comics: []
  };
  var action = arguments.length > 1 ? arguments[1] : undefined;

  switch (action.type) {
    case _comicsConstants.COMICS_TOP_REQUEST:
      return {
        loading: true,
        comics: []
      };

    case _comicsConstants.COMICS_TOP_SUCCESS:
      return {
        loading: false,
        comics: action.payload
      };

    case _comicsConstants.COMICS_TOP_FAIL:
      return {
        loading: false,
        error: action.payload
      };

    default:
      return state;
  }
};

exports.comicsTopRatedReducer = comicsTopRatedReducer;