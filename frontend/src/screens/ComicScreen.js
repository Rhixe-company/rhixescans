import React, { useEffect, useState } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listComicsDetails } from "../actions/comicsActions";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Table, Image } from "react-bootstrap";
import Loader from "../components/ui/Loader";

export const ComicScreen = ({ match }) => {
  const dispatch = useDispatch();
  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { comic } = comicsDetails;
  const [chapters, setChapters] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    dispatch(listComicsDetails(match.params.id));
    fetch(`api/comics/${match.params.id}/chapters/`)
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
        <Table striped bordered hover size="sm" variant="dark">
          <thead>
            <th>TITLE</th>
            <th>IMAGE</th>
            <th>DESCRIPTION</th>
            <th>CATEGORY</th>
            <th>RATING</th>
            <th>STATUS</th>
          </thead>
          <tbody key={comic.id}>
            <tr>
              <td>
                <Link to={`/comic/${comic.id}/`}>{comic.title}</Link>
              </td>
              <td>
                <Link to={`/comic/${comic.id}/`}>
                  <Image
                    src={comic.image}
                    alt={comic.image_url}
                    className="w-full"
                  />
                </Link>
              </td>
              <td>{comic.description}</td>
              <td>{comic.rating}</td>
              <td>{comic.category}</td>
              <td>{comic.status}</td>
            </tr>
          </tbody>
        </Table>
      </div>
      <hr />
      {!isLoading && chapters.length === 0 && (
        <h5 className="text-5xl text-center mx-auto mt-32">
          No Chapters Found
        </h5>
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
