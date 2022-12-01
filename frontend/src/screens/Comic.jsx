import PropTypes from "prop-types";
import React, { useEffect, useState } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { Table } from "react-bootstrap";
import { listComicsDetails } from "../actions/comicsActions";
import Loader from "../components/ui/Loader";

export const Comic = ({ match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();
  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { comic } = comicsDetails;
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dispatch(listComicsDetails(comicId));
    fetch(`api/comics/${comicId}/chapters/`)
      .then((res) => res.json())
      .then((data) => {
        setChapters(data.chapters);
        setLoading(false);
      })
      .catch((err) => console.log(err));
  }, [dispatch, comicId]);
  return (
    <div>
      <div>
        <Table
          striped
          bordered
          hover
          responsive
          className="table-sm align-items-center"
        >
          <thead>
            <tr>
              <th>TITLE</th>
              <th>IMAGE</th>
              <th>DESCRIPTION</th>
              <th>CATEGORY</th>
              <th>RATING</th>
              <th>STATUS</th>
            </tr>
          </thead>
          <tbody key={comic.id}>
            <tr>
              <td>
                <Link to={`/comic/${comic.id}/`}>{comic.title}</Link>
              </td>
              <td>
                <Link to={`/comic/${comic.id}/`}>
                  <img src={comic.image} alt={comic.image_url} />
                </Link>
              </td>
              <td>{comic.description}</td>
              <td>{comic.rating}</td>
              <td>{comic.category}</td>
              <td>{comic.status}</td>
            </tr>
          </tbody>
        </Table>
        <hr />
        {!loading && chapters.length === 0 && <small>No Chapters Found</small>}
        {loading ? (
          <Loader />
        ) : (
          <div>
            <h3>Recent Chapters</h3>
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
    </div>
  );
};

Comic.propTypes = {
  listComicsDetails: PropTypes.func.isRequired,
};

const mapStateToProps = (state) => ({
  comic: state.comicsDetails.comic,
});

export default connect(mapStateToProps, {
  listComicsDetails,
})(Comic);
