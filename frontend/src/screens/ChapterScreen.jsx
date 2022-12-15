import PropTypes from "prop-types";
import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listChaptersDetails } from "../actions/chaptersActions";
import { listComicChapters } from "../actions/comicsActions";
import { Container } from "react-bootstrap";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import ChapterPage from "../components/content/ChapterPage";

export const ChapterScreen = ({ history, match }) => {
  const chapterId = match.params.id;

  const dispatch = useDispatch();
  const chaptersDetails = useSelector((state) => state.chaptersDetails);
  const { chapter, error, loading } = chaptersDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const comicId = chapter?.comics;
  const comicChapters = useSelector((state) => state.comicChapters);
  const { chapters } = comicChapters;
  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    } else {
      if (!chapter.name || chapter.id !== chapterId) {
        dispatch(listChaptersDetails(chapterId));
      }
    }
  }, [dispatch, chapterId, history, userInfo, chapter.name, chapter.id]);

  const chaptersHandler = () => {
    dispatch(listComicChapters(comicId));
  };
  return (
    <div>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container>
          <ChapterPage
            chapter={chapter}
            chapters={chapters}
            chaptersHandler={chaptersHandler}
          />
        </Container>
      )}
    </div>
  );
};

ChapterScreen.propTypes = {
  listChaptersDetails: PropTypes.func.isRequired,
  listComicChapters: PropTypes.func.isRequired,
};

const mapStateToProps = (state) => ({
  chapter: state.chaptersDetails.chapter,
  chapters: state.comicChapters.chapters,
});

export default connect(mapStateToProps, {
  listChaptersDetails,
  listComicChapters,
})(ChapterScreen);
