import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { listComics } from "../actions/comicsActions";
import { Link } from "react-router-dom";
import Paginate from "../components/Paginate";

const IndexScreens = ({ history }) => {
  const dispatch = useDispatch();
  const { comics, page, pages, error, loading } = useSelector(
    (state) => state.comics
  );
  let keyword = history.location.search;

  useEffect(() => {
    dispatch(listComics(keyword));
  }, [dispatch, keyword]);
  return (
    <div>
      {loading ? (
        <span>loading</span>
      ) : error ? (
        <span>{error}</span>
      ) : (
        <div className="card mb-1 box-shadow">
          {comics?.map((comic) => (
            <div className="content-container" key={comic.id}>
              <div className="content">
                <h2>{comic.title}</h2>
                <Link to={`/comic/${comic.id}/`}>
                  <img className="" src={comic.image} alt={comic.image} />
                </Link>
                <div className="content-text">
                  <p>{comic.category}</p>
                </div>
              </div>
            </div>
          ))}
          <Paginate page={page} pages={pages} keyword={keyword} />
        </div>
      )}
    </div>
  );
};

export default IndexScreens;
