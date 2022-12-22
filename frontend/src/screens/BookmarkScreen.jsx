import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Message from "../components/ui/Message";
import { Card, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { addToBookmark, removeFromBookmark } from "../actions/bookmarkActions";
import Rating from "../components/ui/Rating";
const BookmarkScreen = ({ match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();
  const bookmark = useSelector((state) => state.bookmark);
  const { bookmarkItems } = bookmark;

  useEffect(() => {
    if (comicId) {
      dispatch(addToBookmark(comicId));
    }
  }, [dispatch, comicId]);

  const removeFromBookmarkHandler = (id) => {
    dispatch(removeFromBookmark(id));
  };

  return (
    <div>
      <h2>Bookmark</h2>
      {bookmarkItems.length === 0 ? (
        <Message variant="info">
          Your bookmark is empty <Link to="/">Go Back</Link>
        </Message>
      ) : (
        <div>
          {bookmarkItems.map((item) => (
            <Card className="my-3 p-3 rounded">
              <Link to={`/comic/${item.id}/`}>
                <Card.Img src={item.image} />
              </Link>
              <Card.Body>
                <Link to={`/comic/${item.id}/`}>
                  <Card.Title as="div">
                    <strong>{item.title}</strong>
                  </Card.Title>
                </Link>

                <Card.Text>
                  <div className="my-3">
                    <Rating
                      value={item.rating}
                      text={` ${item.rating} `}
                      color={"#f8e825"}
                    />
                  </div>
                </Card.Text>
                <Card.Text as="div">
                  Description:
                  <p>{item.description}</p>
                </Card.Text>

                <Card.Text as="div">
                  <b>Status:</b>
                  {item.status}
                </Card.Text>

                <Card.Text as="div">
                  <div className="my-3">
                    <b>Artist:</b>
                    {item.artist}
                  </div>
                </Card.Text>
                <Card.Text as="div">
                  <div className="my-3">
                    <b>Author:</b>
                    {item.author}
                  </div>
                </Card.Text>

                <Card.Text as="div">
                  <b>Category:</b>
                  <span>{item.category}</span>
                </Card.Text>
                <Card.Text as="div">
                  <div className="my-3">
                    <b>Release Date:</b>
                    {item.release_date}
                  </div>
                </Card.Text>

                <Card.Text as="div">
                  <b>Last Updated:</b>
                  {new Date(item.updated).toLocaleString("en-US")}
                </Card.Text>
                <Button
                  type="button"
                  variant="light"
                  onClick={() => removeFromBookmarkHandler(item.id)}
                >
                  <i className="fas fa-trash"></i>
                </Button>
                {item.genres?.map((genre, index) => (
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
          ))}
        </div>
      )}
    </div>
  );
};

export default BookmarkScreen;
