import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";
import { listComicsDetails } from "../actions/comicsActions";
import Rating from "../components/ui/Rating";
import {
  Form,
  Button,
  Row,
  Col,
  Image,
  ListGroup,
  Card,
} from "react-bootstrap";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Link } from "react-router-dom";
import { removeFromBookmark, addToBookmark } from "../actions/bookmarkActions";

export const ComicScreen = ({ history, match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();

  const bookmark = useSelector((state) => state.bookmark);
  const { bookmarkItems } = bookmark;

  const { comic, error, loading, chapters } = useSelector(
    (state) => state.comicsDetails
  );
  const { userInfo } = useSelector((state) => state.userLogin);
  const genres = comic.genres;

  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    }
    dispatch(listComicsDetails(comicId));
  }, [history, userInfo, dispatch, comicId]);

  const removeFromBookmarkHandler = (e) => {
    dispatch(removeFromBookmark(comic.id));
    history.push(`/comic/${comic.id}/`);
  };

  const addToBookmarkHandler = (e) => {
    dispatch(addToBookmark(comic.id));
    e.preventDefault();
  };
  for (let index = 0; index < bookmarkItems.length; index++) {
    const elementid = bookmarkItems[index].id;
    const elementtitle = bookmarkItems[index].title;
    console.log(elementid, elementtitle);
  }

  return (
    <div>
      <Link to="/" className="btn btn-light my-3">
        Go Back
      </Link>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <div>
          <Row>
            <div></div>
            <Col md={6}>
              <Link to={`/comic/${comic.id}/`}>
                <Image fluid="true" src={comic.image} alt={comic.image} />
              </Link>

              {bookmarkItems.length === 0 ? (
                <Form onSubmit={addToBookmarkHandler}>
                  <Button type="submit" id="bookmark" variant="primary">
                    Add Bookmark
                  </Button>
                </Form>
              ) : (
                <Form onSubmit={removeFromBookmarkHandler}>
                  <Button type="submit" variant="primary">
                    Remove Bookmark
                  </Button>
                </Form>
              )}
              <Card key={comic.id} className="my-3 p-3 rounded">
                <Card.Body className="px-6 py-4">
                  <Link to={`/comic/${comic.id}/`}>
                    <Card.Title as="div">
                      <h2 className="font-bold text-black-500 text-xl mb-2">
                        {comic.title}
                      </h2>
                    </Card.Title>
                  </Link>
                  <Card.Text as="div">
                    <div className="my-3">
                      <b>Rating:</b>

                      <Rating
                        value={comic.rating}
                        text={` ${comic.rating} `}
                        color={"#f8e825"}
                      />
                    </div>
                  </Card.Text>

                  <Card.Text as="div">
                    Description:
                    <p>{comic.description}</p>
                  </Card.Text>

                  <Card.Text as="div">
                    <b>Status:</b>
                    {comic.status}
                  </Card.Text>

                  <Card.Text as="div">
                    <div className="my-3">
                      <b>Artist:</b>
                      {comic.artist}
                    </div>
                  </Card.Text>
                  <Card.Text as="div">
                    <div className="my-3">
                      <b>Author:</b>
                      {comic.author}
                    </div>
                  </Card.Text>

                  <Card.Text as="div">
                    <b>Category:</b>
                    <span>{comic.category}</span>
                  </Card.Text>
                  <Card.Text as="div">
                    <div className="my-3">
                      <b>Release Date:</b>
                      {comic.release_date}
                    </div>
                  </Card.Text>

                  <Card.Text as="div">
                    <b>Last Updated:</b>
                    {new Date(comic.updated).toLocaleString("en-US")}
                  </Card.Text>

                  {genres?.map((genre, index) => (
                    <Card.Text
                      as="div"
                      key={index}
                      className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
                    >
                      <span>{genre.name}</span>
                    </Card.Text>
                  ))}
                </Card.Body>
              </Card>
            </Col>
            <Col>
              <br />
              {chapters?.length > 0 ? (
                <div>
                  <b>Total Chapters: {comic.numChapters}</b>

                  {chapters?.map((chapter) => (
                    <ListGroup key={chapter.id}>
                      <ListGroup.Item>
                        <Link to={`/comics/chapter/${chapter.id}/`}>
                          <span>{chapter.name}</span>
                        </Link>
                      </ListGroup.Item>
                    </ListGroup>
                  ))}
                </div>
              ) : (
                <div>No Chapter Found</div>
              )}
            </Col>
          </Row>
        </div>
      )}
    </div>
  );
};

ComicScreen.propTypes = {
  listComicsDetails: PropTypes.func.isRequired,
};
const mapStateToProps = (state) => ({
  comic: state.comicsDetails.comic,
});

export default connect(mapStateToProps, {
  listComicsDetails,
})(ComicScreen);
