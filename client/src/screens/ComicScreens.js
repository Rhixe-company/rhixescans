import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { listComicDetails } from "../actions/comicsActions";
import Bookmark from "../components/Bookmark";
import { Link } from "react-router-dom";

const ComicScreens = ({ match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();
  const { comic, error, loading, chapters } = useSelector(
    (state) => state.comic
  );
  useEffect(() => {
    dispatch(listComicDetails(comicId));
  }, [dispatch, comicId]);
  console.log(chapters);
  return (
    <div className="App">
      {loading ? (
        <span>loading...</span>
      ) : error ? (
        <div>{error}</div>
      ) : (
        <div className="comic-container card">
          <div className="card-header">
            <h2>{comic?.title}</h2>
            <img
              className="img-fluid rounded"
              src={comic?.image}
              alt={comic?.image}
            />
          </div>
          <Bookmark likes={comic?.likes} bookmarks={comic?.favourites} />
          <div className="card-body">
            <p className="card-title">{comic?.description}</p>
            <em className="card-text">{comic?.rating}</em>
            <table className="table">
              <thead>
                <tr>
                  <th>Author</th>
                  <th>Artist</th>
                  <th>Category</th>
                  <th>Status</th>
                  <th>Released</th>
                  <th>Published Date</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{comic?.author}</td>
                  <td>{comic?.artist}</td>
                  <td>{comic?.category}</td>
                  <td>{comic?.status}</td>
                  <td>{comic?.released}</td>
                  <td>{Date(comic?.created)}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="card-footer">
            <ul className="list-group listgroup-flush">
              {chapters?.map((chapter) => (
                <li key={chapter.id} className="list-group-item">
                  <Link to={`/chapter/${chapter.id}/`}>{chapter.name}</Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComicScreens;
