import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listComicsDetails, listComicChapters } from "../actions/comicsActions";
import Comicgrid from "../components/content/Comicgrid";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Link } from "react-router-dom";
import { Container, Button } from "react-bootstrap";

export const ComicScreen = ({ history, match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();
  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { comic, error, loading } = comicsDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const comicChapters = useSelector((state) => state.comicChapters);
  const { chapters } = comicChapters;
  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    }
    dispatch(listComicsDetails(comicId));
    dispatch(listComicChapters(comicId));
  }, [history, userInfo, dispatch, comicId]);
  return (
    <Container>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <div>
          <Link to="/">
            <Button>Go Back Home</Button>
          </Link>
          <Comicgrid comic={comic} />
          <br />
          {chapters.length > 0 ? (
            <div>
              Total Chapters: {comic.numChapters}
              <hr />
              {chapters?.map((chapter) => (
                <ul key={chapter.id}>
                  <li>
                    <Link to={`/comics/chapter/${chapter.id}/`}>
                      <h3>{chapter.name}</h3>
                    </Link>
                    <div>
                      {new Date(chapter.updated).toLocaleString("en-US")}
                    </div>
                  </li>
                </ul>
              ))}
            </div>
          ) : (
            <h3>No Chapters Created</h3>
          )}
        </div>
      )}
    </Container>
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
