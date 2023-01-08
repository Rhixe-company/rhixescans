import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { listChapterDetails } from "../actions/chaptersActions";
import { Link } from "react-router-dom";
const ChapterScreens = ({ match }) => {
  const chapterId = match.params.id;
  const dispatch = useDispatch();
  const { chapter, comic, error, loading, chapters } = useSelector(
    (state) => state.chapter
  );
  useEffect(() => {
    dispatch(listChapterDetails(chapterId));
  }, [dispatch, chapterId]);
  const pages = chapter?.pages;
  return (
    <div>
      {loading ? (
        <span>loading...</span>
      ) : error ? (
        <div>{error}</div>
      ) : (
        <>
          <div className="chapter-container">
            <Link to={`/comic/${comic?.id}/`}>
              <h2>{comic?.title}</h2>
            </Link>
            <p>{chapter?.name}</p>
            {pages.map((page, index) => (
              <div key={index}>
                <img src={page.images} alt={page.images_url} />
              </div>
            ))}
          </div>
          <ul className="list-group listgroup-flush">
            {chapters?.map((chapter) => (
              <li key={chapter.id} className="list-group-item">
                <Link to={`/chapter/${chapter.id}/`}>{chapter.name}</Link>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export default ChapterScreens;
