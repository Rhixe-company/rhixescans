import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listComicsDetails, listComicChapters } from "../actions/comicsActions";
import Comicgrid from "../components/content/Comicgrid";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Link } from "react-router-dom";
import { Button } from "react-bootstrap";

export const ComicScreen = ({ match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();
  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { comic, error, loading } = comicsDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const comicChapters = useSelector((state) => state.comicChapters);
  const { chapters } = comicChapters;
  useEffect(() => {
    dispatch(listComicsDetails(comicId));
    dispatch(listComicChapters(comicId));
  }, [dispatch, comicId]);
  return (
    <div>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <div>
          {userInfo ? (
            <div>
              <Link to="/">
                <Button>Go Back Home</Button>
              </Link>
              <Comicgrid comic={comic} />

              <div>
                Total Chapters: {comic.numChapters}
                <br />
              </div>
              <hr />
              {chapters?.map((chapter) => (
                <Link key={chapter?.id} to={`/comics/chapter/${chapter.id}/`}>
                  <Button variant="outline-dark" size="sm">
                    {chapter?.name}
                  </Button>
                </Link>
              ))}
            </div>
          ) : (
            <Link to="/login">
              <Button>Please Login To Read Comic</Button>
            </Link>
          )}
        </div>
      )}
    </div>
  );
};

const mapStateToProps = (state) => ({
  comic: state.comicsDetails.comic,
  chapters: state.comicChapters.chapters,
});

export default connect(mapStateToProps, {
  listComicsDetails,
  listComicChapters,
})(ComicScreen);
