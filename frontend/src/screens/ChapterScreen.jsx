import { Container } from "react-bootstrap";
import React, { useEffect } from "react";
import PropTypes from "prop-types";
import { listChaptersDetails } from "../actions/chaptersActions";

import Pages from "../components/content/Pages";
import PagesPagination from "../components/content/PagesPagination";
import { connect, useDispatch, useSelector } from "react-redux";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Link } from "react-router-dom";
import { Button } from "react-bootstrap";
export const ChapterScreen = ({ match, history }) => {
  const chapterId = match.params.id;

  const dispatch = useDispatch();
  const chaptersDetails = useSelector((state) => state.chaptersDetails);
  const { comic, chapter, error, loading } = chaptersDetails;

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    } else {
      if (!chapter.comics) {
      }
      dispatch(listChaptersDetails(chapterId));
    }
  }, [userInfo, history, dispatch, chapterId, chapter.comics]);

  return (
    <Container>
      <div className="container mx-auto">
        <div>
          {loading ? (
            <Loader />
          ) : error ? (
            <Message variant="danger">{error}</Message>
          ) : (
            <div>
              <Link to={`/comic/${comic?.id}/`}>{comic?.title}</Link>

              <div className="container mx-auto">
                <Link to={`/comic/${chapter.comics}/`}>
                  <Button variant="secondary">{chapter.name}</Button>
                </Link>
                {chapter.pages?.map((page) => (
                  <Pages page={page} key={page.id} />
                ))}
              </div>
              <Link to={`/comic/${comic?.id}/`}>{comic?.title}</Link>
              {comic?.chapters?.map((chapter) => (
                <PagesPagination chapter={chapter} key={chapter.id} />
              ))}
            </div>
          )}
        </div>
      </div>
    </Container>
  );
};

ChapterScreen.propTypes = {
  listChaptersDetails: PropTypes.func.isRequired,
};
const mapStateToProps = (state) => ({
  chapter: state.chaptersDetails.chapter,
  comic: state.chaptersDetails.comic,
});

export default connect(mapStateToProps, {
  listChaptersDetails,
})(ChapterScreen);
