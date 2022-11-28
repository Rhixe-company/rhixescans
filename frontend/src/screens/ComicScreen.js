import React, { useEffect, useState } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listComicsDetails } from "../actions/comicsActions";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Card } from "react-bootstrap";
import Rating from "../components/ui/Rating";
import Loader from "../components/ui/Loader";

export const ComicScreen = ({ match }) => {
  const dispatch = useDispatch();
  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { comic } = comicsDetails;
  const [chapters, setChapters] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    dispatch(listComicsDetails(match.params.id));
    fetch(`api/comics/${match.params.id}/chapters`)
      .then((res) => res.json())
      .then((data) => {
        setChapters(data.chapters);
        setIsLoading(false);
        console.log(data);
      })
      .catch((err) => console.log(err));
  }, [dispatch, match]);
  return (
    <div>
      <div>
        <Card className="my-3 p-3 rounded">
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
            <Card.Text as="span">{comic.category}</Card.Text>
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
          </Card.Body>
        </Card>
      </div>
      <hr />
      {!isLoading && chapters.length === 0 && (
        <strong className="text-5xl text-center mx-auto mt-32">
          No Chapters Found
        </strong>
      )}
      {isLoading ? (
        <Loader />
      ) : (
        <div>
          {chapters.map((chapter) => (
            <ul key={chapter.id}>
              <li>
                <Link to={`/comics/chapter/${chapter.id}/`}>
                  <span>{chapter?.name}</span>
                  <span>{chapter?.created}</span>
                </Link>
              </li>
            </ul>
          ))}
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

export default connect(mapStateToProps, { listComicsDetails })(ComicScreen);
