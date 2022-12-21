import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { listChaptersDetails } from "../actions/chaptersActions";
import { listComicsDetails } from "../actions/comicsActions";
import Pagination from "../components/Pagination";
import Pages from "../components/content/Pages";
import { connect, useDispatch, useSelector } from "react-redux";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Link } from "react-router-dom";
import { Button, Col, ListGroup, Row } from "react-bootstrap";
export const ChapterScreen = ({ match, history }) => {
  const chapterId = match.params.id;

  const dispatch = useDispatch();
  const chaptersDetails = useSelector((state) => state.chaptersDetails);
  const { comic, chapter, error, loading } = chaptersDetails;

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const { chapters } = useSelector((state) => state.comicsDetails);
  const [currentPage, setCurrentPage] = useState(1);
  const [postsPerPage] = useState(50);
  const comicId = chapter?.comics;
  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    } else {
      dispatch(listChaptersDetails(chapterId));
      if (comicId) {
        dispatch(listComicsDetails(comicId));
      }
    }
  }, [userInfo, history, dispatch, chapterId, comicId]);
  const pages = chapter?.pages;

  // Get current posts
  const indexOfLastPost = currentPage * postsPerPage;
  const indexOfFirstPost = indexOfLastPost - postsPerPage;
  const currentPosts = chapters?.slice(indexOfFirstPost, indexOfLastPost);
  // Chage page
  const paginate = (pageNumber) => setCurrentPage(pageNumber);
  return (
    <Row>
      <Link to={`/comic/${comic?.id}/`} className="btn btn-dark my-3">
        Go Back
      </Link>

      <div>
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <Col>
            <div>
              {chapter.name}

              {pages?.map((page) => (
                <Pages page={page} key={page.id} />
              ))}
            </div>

            <Link to={`/comic/${chapter?.comics}/`}>
              <Button variant="primary"> {chapter?.name}</Button>
            </Link>
          </Col>
        )}
        {currentPosts?.map((post) => (
          <ListGroup key={post.id} className="list-group-item">
            <ListGroup.Item>
              <Link to={`/comics/chapter/${post.id}/`}>
                <span>{post.name}</span>
              </Link>
            </ListGroup.Item>
          </ListGroup>
        ))}
        <Pagination
          postsPerPage={postsPerPage}
          totalPosts={comic?.chapters?.length}
          paginate={paginate}
        />
      </div>
    </Row>
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
