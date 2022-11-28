import React, { Component } from "react";
import { Card } from "react-bootstrap";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import Rating from "../ui/Rating";
import { Link } from "react-router-dom";
import { listComics } from "../../actions/comicsActions";

export class Posts extends Component {
  componentDidMount() {
    this.props.listComics();
  }
  render() {
    const comicsItems = this.props.comics.map((comic) => (
      <section>
        <Card key={comic.id} className="my-3 p-3 rounded">
          <Card.Body className="px-6 py-4">
            <Link to={`/comic/${comic.id}/`}>
              <Card.Title
                as="div"
                className="font-bold text-black-500 text-xl mb-2"
              >
                <strong>{comic.title}</strong>
              </Card.Title>
            </Link>
            <Link to={`/comic/${comic.id}/`}>
              <Card.Img src={comic.image} alt="" className="w-full" />
            </Link>
            <br></br>
            <Card.Text as="span">
              Category:
              {comic.category}
            </Card.Text>
            <Card.Text as="div">
              <div className="my-3">
                <Rating
                  value={comic.rating}
                  text={`${comic.rating} `}
                  color={"#f8e825"}
                />
              </div>
            </Card.Text>
            <br />
            {comic.genres.map((genre) => (
              <div key={genre?.id}>
                <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2">
                  #{genre?.name}
                </span>
              </div>
            ))}
            <br />
          </Card.Body>

          {comic.chapters.map((chapter) => (
            <div key={chapter?.id}>
              <Link to={`/comics/chapter/${chapter.id}/`}>
                <small>{chapter?.name}</small>
              </Link>
              <hr />
            </div>
          ))}
        </Card>
      </section>
    ));
    return <div className="grid grid-cols-2 gap-3">{comicsItems}</div>;
  }
}

Posts.propTypes = {
  listComics: PropTypes.func.isRequired,
  comics: PropTypes.array.isRequired,
};

const mapStateToProps = (state) => ({
  comics: state.comicsList.comics,
});

export default connect(mapStateToProps, { listComics })(Posts);
