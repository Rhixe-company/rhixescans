import PropTypes from "prop-types";
import React, { Component } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { Pagination } from "react-bootstrap";
import { listComics } from "../actions/comicsActions";

export class indexScreens extends Component {
  componentDidMount() {
    this.props.listComics();
  }
  render() {
    const Items = this.props.comics?.map((comic) => (
      <div className="content-container" key={comic.id}>
        <div className="content">
          <h2>{comic.title}</h2>
          <Link to={`/comic/${comic.id}/`}>
            <img src={comic.image} alt={comic.image} />
          </Link>
          <div className="content-text">
            <p>{comic.category}</p>
          </div>
        </div>
      </div>
    ));
    return (
      <>
        <div>{Items}</div>
        {this.props.pages > 1 && (
          <Pagination size="sm">
            {[...Array(this.props.pages).keys()].map((x) => (
              <a key={x + 1} href={`&page=${x + 1}`}>
                <Pagination.Item active={x + 1 === this.props.page}>
                  {x + 1}
                </Pagination.Item>
              </a>
            ))}
          </Pagination>
        )}
      </>
    );
  }
}

indexScreens.propTypes = {
  listComics: PropTypes.func.isRequired,
};

const mapStateToProps = (state) => ({
  comics: state.comics.comics,
  page: state.comics.page,
  pages: state.comics.pages,
});

export default connect(mapStateToProps, { listComics })(indexScreens);
