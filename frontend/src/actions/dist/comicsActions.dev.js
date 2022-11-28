"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.updateComic = exports.createComic = exports.deleteComic = exports.listComicsDetails = exports.listTopComics = exports.listComics = void 0;

var _axios = _interopRequireDefault(require("axios"));

var _comicsConstants = require("../constants/comicsConstants");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

var listComics = function listComics() {
  var keyword = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "";
  return function _callee(dispatch) {
    var _ref, data;

    return regeneratorRuntime.async(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            _context.prev = 0;
            dispatch({
              type: _comicsConstants.COMICS_LIST_REQUEST
            });
            _context.next = 4;
            return regeneratorRuntime.awrap(_axios["default"].get("/api/comics".concat(keyword)));

          case 4:
            _ref = _context.sent;
            data = _ref.data;
            dispatch({
              type: _comicsConstants.COMICS_LIST_SUCCESS,
              payload: data
            });
            _context.next = 12;
            break;

          case 9:
            _context.prev = 9;
            _context.t0 = _context["catch"](0);
            dispatch({
              type: _comicsConstants.COMICS_LIST_FAIL,
              payload: _context.t0.response && _context.t0.response.data.detail ? _context.t0.response.data.detail : _context.t0.message
            });

          case 12:
          case "end":
            return _context.stop();
        }
      }
    }, null, null, [[0, 9]]);
  };
};

exports.listComics = listComics;

var listTopComics = function listTopComics() {
  return function _callee2(dispatch) {
    var _ref2, data;

    return regeneratorRuntime.async(function _callee2$(_context2) {
      while (1) {
        switch (_context2.prev = _context2.next) {
          case 0:
            _context2.prev = 0;
            dispatch({
              type: _comicsConstants.COMICS_TOP_REQUEST
            });
            _context2.next = 4;
            return regeneratorRuntime.awrap(_axios["default"].get("/api/comics/top/"));

          case 4:
            _ref2 = _context2.sent;
            data = _ref2.data;
            dispatch({
              type: _comicsConstants.COMICS_TOP_SUCCESS,
              payload: data
            });
            _context2.next = 12;
            break;

          case 9:
            _context2.prev = 9;
            _context2.t0 = _context2["catch"](0);
            dispatch({
              type: _comicsConstants.COMICS_TOP_FAIL,
              payload: _context2.t0.response && _context2.t0.response.data.detail ? _context2.t0.response.data.detail : _context2.t0.message
            });

          case 12:
          case "end":
            return _context2.stop();
        }
      }
    }, null, null, [[0, 9]]);
  };
};

exports.listTopComics = listTopComics;

var listComicsDetails = function listComicsDetails(id) {
  return function _callee3(dispatch) {
    var _ref3, data;

    return regeneratorRuntime.async(function _callee3$(_context3) {
      while (1) {
        switch (_context3.prev = _context3.next) {
          case 0:
            _context3.prev = 0;
            dispatch({
              type: _comicsConstants.COMICS_DETAILS_REQUEST
            });
            _context3.next = 4;
            return regeneratorRuntime.awrap(_axios["default"].get("/api/comics/".concat(id)));

          case 4:
            _ref3 = _context3.sent;
            data = _ref3.data;
            dispatch({
              type: _comicsConstants.COMICS_DETAILS_SUCCESS,
              payload: data
            });
            _context3.next = 12;
            break;

          case 9:
            _context3.prev = 9;
            _context3.t0 = _context3["catch"](0);
            dispatch({
              type: _comicsConstants.COMICS_DETAILS_FAIL,
              payload: _context3.t0.response && _context3.t0.response.data.detail ? _context3.t0.response.data.detail : _context3.t0.message
            });

          case 12:
          case "end":
            return _context3.stop();
        }
      }
    }, null, null, [[0, 9]]);
  };
};

exports.listComicsDetails = listComicsDetails;

var deleteComic = function deleteComic(id) {
  return function _callee4(dispatch, getState) {
    var _getState, userInfo, config, _ref4, data;

    return regeneratorRuntime.async(function _callee4$(_context4) {
      while (1) {
        switch (_context4.prev = _context4.next) {
          case 0:
            _context4.prev = 0;
            dispatch({
              type: _comicsConstants.COMICS_DELETE_REQUEST
            });
            _getState = getState(), userInfo = _getState.userLogin.userInfo;
            config = {
              headers: {
                "Content-type": "application/json",
                Authorization: "Bearer ".concat(userInfo.token)
              }
            }; // eslint-disable-next-line no-unused-vars

            _context4.next = 6;
            return regeneratorRuntime.awrap(_axios["default"]["delete"]("/api/comics/delete/".concat(id, "/"), config));

          case 6:
            _ref4 = _context4.sent;
            data = _ref4.data;
            dispatch({
              type: _comicsConstants.COMICS_DELETE_SUCCESS
            });
            _context4.next = 14;
            break;

          case 11:
            _context4.prev = 11;
            _context4.t0 = _context4["catch"](0);
            dispatch({
              type: _comicsConstants.COMICS_DELETE_FAIL,
              payload: _context4.t0.response && _context4.t0.response.data.detail ? _context4.t0.response.data.detail : _context4.t0.message
            });

          case 14:
          case "end":
            return _context4.stop();
        }
      }
    }, null, null, [[0, 11]]);
  };
};

exports.deleteComic = deleteComic;

var createComic = function createComic() {
  return function _callee5(dispatch, getState) {
    var _getState2, userInfo, config, _ref5, data;

    return regeneratorRuntime.async(function _callee5$(_context5) {
      while (1) {
        switch (_context5.prev = _context5.next) {
          case 0:
            _context5.prev = 0;
            dispatch({
              type: _comicsConstants.COMICS_CREATE_REQUEST
            });
            _getState2 = getState(), userInfo = _getState2.userLogin.userInfo;
            config = {
              headers: {
                "Content-type": "application/json",
                Authorization: "Bearer ".concat(userInfo.token)
              }
            };
            _context5.next = 6;
            return regeneratorRuntime.awrap(_axios["default"].post("/api/comics/create/", {}, config));

          case 6:
            _ref5 = _context5.sent;
            data = _ref5.data;
            dispatch({
              type: _comicsConstants.COMICS_CREATE_SUCCESS,
              payload: data
            });
            _context5.next = 14;
            break;

          case 11:
            _context5.prev = 11;
            _context5.t0 = _context5["catch"](0);
            dispatch({
              type: _comicsConstants.COMICS_CREATE_FAIL,
              payload: _context5.t0.response && _context5.t0.response.data.detail ? _context5.t0.response.data.detail : _context5.t0.message
            });

          case 14:
          case "end":
            return _context5.stop();
        }
      }
    }, null, null, [[0, 11]]);
  };
};

exports.createComic = createComic;

var updateComic = function updateComic(comic) {
  return function _callee6(dispatch, getState) {
    var _getState3, userInfo, config, _ref6, data;

    return regeneratorRuntime.async(function _callee6$(_context6) {
      while (1) {
        switch (_context6.prev = _context6.next) {
          case 0:
            _context6.prev = 0;
            dispatch({
              type: _comicsConstants.COMICS_UPDATE_REQUEST
            });
            _getState3 = getState(), userInfo = _getState3.userLogin.userInfo;
            config = {
              headers: {
                "Content-type": "application/json",
                Authorization: "Bearer ".concat(userInfo.token)
              }
            };
            _context6.next = 6;
            return regeneratorRuntime.awrap(_axios["default"].put("/api/comics/update/".concat(comic.id, "/"), comic, config));

          case 6:
            _ref6 = _context6.sent;
            data = _ref6.data;
            dispatch({
              type: _comicsConstants.COMICS_UPDATE_SUCCESS,
              payload: data
            });
            dispatch({
              type: _comicsConstants.COMICS_DETAILS_SUCCESS,
              payload: data
            });
            _context6.next = 15;
            break;

          case 12:
            _context6.prev = 12;
            _context6.t0 = _context6["catch"](0);
            dispatch({
              type: _comicsConstants.COMICS_UPDATE_FAIL,
              payload: _context6.t0.response && _context6.t0.response.data.detail ? _context6.t0.response.data.detail : _context6.t0.message
            });

          case 15:
          case "end":
            return _context6.stop();
        }
      }
    }, null, null, [[0, 12]]);
  };
};

exports.updateComic = updateComic;