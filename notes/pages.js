import React, { Component } from "react";
import { connect } from "react-redux";
import { listComics } from "../actions/comicsActions";

export class Page extends Component {
  componentDidMount() {
    this.props.listComics();
  }
  render() {
    return (
      <div>
        <h1>Page</h1>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  comics: state.comicsList.comics,
});

export default connect(mapStateToProps, { listComics })(Page);
