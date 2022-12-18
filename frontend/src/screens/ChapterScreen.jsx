import { Container } from "react-bootstrap";
import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { listChaptersDetails } from "../actions/chaptersActions";

import Pagination from "../components/Pagination";
import Pages from "../components/content/Pages";
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
  const [currentPage, setCurrentPage] = useState(1);
  const [postsPerPage] = useState(50);

  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    } else {
      if (!chapter?.comics) {
      }
      dispatch(listChaptersDetails(chapterId));
    }
  }, [userInfo, history, dispatch, chapterId, chapter?.comics]);
  const pages = chapter?.pages;

  // Get current posts
  const indexOfLastPost = currentPage * postsPerPage;
  const indexOfFirstPost = indexOfLastPost - postsPerPage;
  const currentPosts = comic?.chapters?.slice(
    indexOfFirstPost,
    indexOfLastPost
  );
  // Chage page
  const paginate = (pageNumber) => setCurrentPage(pageNumber);
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
                {pages?.map((page, index) => (
                  <Pages page={page} key={index} />
                ))}
              </div>
              <Link to={`/comic/${chapter?.comics}/`}>{chapter?.name}</Link>
            </div>
          )}
        </div>
        <ul className="list-group mb-4">
          {currentPosts?.map((post) => (
            <li key={post.id} className="list-group-item">
              <Link to={`/comics/chapter/${post.id}/`}>{post.name}</Link>
            </li>
          ))}
        </ul>
        <Pagination
          postsPerPage={postsPerPage}
          totalPosts={comic?.chapters?.length}
          paginate={paginate}
        />
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
