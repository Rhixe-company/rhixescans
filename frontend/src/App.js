import React, { Component, Fragment } from "react";
import { Container } from "react-bootstrap";
import { HashRouter as Router, Route } from "react-router-dom";

import Header from "./components/ui/Header";
import Footer from "./components/ui/Footer";

import LoginScreen from "./screens/LoginScreen";
import RegisterScreen from "./screens/RegisterScreen";
import ProfileScreen from "./screens/ProfileScreen";
import UserListScreen from "./screens/UserListScreen";
import UserEditScreen from "./screens/UserEditScreen";
import ComicScreen from "./screens/ComicScreen";
import ComicsEditScreen from "./screens/ComicsEditScreen";
import ChaptersListScreen from "./screens/ChaptersListScreen";
import ChaptersEditScreen from "./screens/ChaptersEditScreen";
import PostsScreen from "./screens/PostsScreen";
import ChapterScreen from "./screens/ChapterScreen";
import ComicsListScreen from "./screens/ComicsListScreen";

class App extends Component {
  render() {
    return (
      <Fragment>
        <Router>
          <Header />
          <div className="container">
            <Container>
              <Route path="/" component={PostsScreen} exact />
              <Route path="/comic/:id/" component={ComicScreen} />
              <Route path="/comics/chapter/:id/" component={ChapterScreen} />
              <Route path="/login" component={LoginScreen} />
              <Route path="/register" component={RegisterScreen} />
              <Route path="/profile" component={ProfileScreen} />
              <Route path="/admin/users" component={UserListScreen} />
              <Route path="/admin/user/:id/edit" component={UserEditScreen} />
              <Route path="/admin/comics" component={ComicsListScreen} />
              <Route
                path="/admin/comic/:id/edit"
                component={ComicsEditScreen}
              />
              <Route path="/admin/chapters" component={ChaptersListScreen} />
              <Route
                path="/admin/chapter/:id/edit"
                component={ChaptersEditScreen}
              />
            </Container>
          </div>
          <Footer />
        </Router>
      </Fragment>
    );
  }
}

export default App;
