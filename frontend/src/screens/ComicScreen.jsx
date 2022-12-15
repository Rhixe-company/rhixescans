import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listComicsDetails, listComicChapters } from "../actions/comicsActions";
import Comicgrid from "../components/content/Comicgrid";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";

import { Container } from "react-bootstrap";

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
    <section>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container>
          <Comicgrid comic={comic} chapters={chapters} />
        </Container>
      )}
    </section>
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
