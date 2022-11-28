import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { listComics, deleteComic } from "../../actions/comicsActions";
import { Image, Table } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

export class Comics extends Component {
  static propTypes = {
    listComics: PropTypes.func.isRequired,
    deleteComic: PropTypes.func.isRequired,
    comics: PropTypes.array.isRequired,
  };
  componentDidMount() {
    this.props.listComics();
  }

  render() {
    return (
      <Fragment>
        <Table striped bordered hover responsive className="table-lg">
          <thead>
            <tr>
              <th>TITLE</th>
              <th>IMAGE</th>
              <th>DESCRIPTION</th>
              <th>CATEGORY</th>
              <th>RATING</th>
              <th>STATUS</th>
              <th />
              <th />
            </tr>
          </thead>

          <tbody>
            {this.props.comics.map((comic) => (
              <>
                <tr key={comic.id}>
                  <td>{comic.title}</td>
                  <td>
                    <Image src={comic.image} alt={comic.image_url} fluid />
                  </td>
                  <td>{comic.description}</td>
                  <td>{comic.rating}</td>
                  <td>{comic.category}</td>
                  <td>{comic.status}</td>
                  <td>{comic.author}</td>
                  <td>
                    <LinkContainer to={`/admin/comic/${comic.id}/edit`}>
                      <button>
                        <i className="fas fa-edit">Edit</i>
                      </button>
                    </LinkContainer>
                  </td>
                  <td>
                    <button
                      onClick={this.props.deleteComic.bind(this, comic.id)}
                      className="btn btn-danger btn-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </>
            ))}
          </tbody>
        </Table>
      </Fragment>
    );
  }
}

const mapStateToProps = (state) => ({
  comics: state.comicsList.comics,
});

export default connect(mapStateToProps, { listComics, deleteComic })(Comics);
