import React, { Component } from "react";
import { HashRouter as Router, Route } from "react-router-dom";
import IndexScreens from "./screens/IndexScreens";
import ComicScreens from "./screens/ComicScreens";
import Header from "./components/Header";
import ChapterScreens from "./screens/ChapterScreens";
export class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Header />
          <Route path="/" component={IndexScreens} exact />
          <Route path="/comic/:id/" component={ComicScreens} />
          <Route path="/chapter/:id/" component={ChapterScreens} />
        </div>
      </Router>
    );
  }
}

export default App;
