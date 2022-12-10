import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listChaptersDetails } from "../actions/chaptersActions";
import { listComicsDetails } from "../actions/comicsActions";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Link } from "react-router-dom";
import { Button, Container, Image } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroll-component";

export const ChaptersScreen = ({ match }) => {
  const chapterId = match.params.id;
  const dispatch = useDispatch();
  const chaptersDetails = useSelector((state) => state.chaptersDetails);
  const { chapter, error, loading } = chaptersDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { comic } = comicsDetails;

  useEffect(() => {
    dispatch(listChaptersDetails(chapterId));
    dispatch(listComicsDetails(chapter?.comics));
  }, [dispatch, chapterId, chapter?.comics]);
  return (
    <div>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <>
          {userInfo ? (
            <Container>
              <div>
                <Link to={`/comic/${chapter.comics}/`}>
                  <h1>{chapter?.name}</h1>
                </Link>

                {chapter.pages?.map((page) => (
                  <InfiniteScroll
                    dataLength={page}
                    key={page.id}
                    className="pages"
                  >
                    <Image
                      className="page"
                      src={page.images}
                      alt={page.images_url}
                    />
                  </InfiniteScroll>
                ))}
              </div>
              <Link to={`/comic/${chapter.comics}/`}>
                <Button>
                  <span>{comic?.title}</span>
                </Button>
              </Link>
            </Container>
          ) : (
            <Link to="/login">
              <Button>Please Login To Read Comic</Button>
            </Link>
          )}
        </>
      )}
    </div>
  );
};

const mapStateToProps = (state) => ({
  chapter: state.chaptersDetails.chapter,
  comic: state.comicsDetails.comic,
});

export default connect(mapStateToProps, {
  listComicsDetails,
  listChaptersDetails,
})(ChaptersScreen);
