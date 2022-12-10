import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listChaptersDetails } from "../actions/chaptersActions";
import { listComicChapters } from "../actions/comicsActions";

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
  const comicChapters = useSelector((state) => state.comicChapters);
  const { chapters, isLoading } = comicChapters;

  useEffect(() => {
    dispatch(listChaptersDetails(chapterId));
    dispatch(listComicChapters(chapter?.comics));
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
                <Button variant="dark">
                  <Link to={`/comic/${chapter.comics}/`}>{chapter.name}</Link>
                </Button>

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
                <Button variant="dark">
                  <Link to={`/comic/${chapter.comics}/`}>Go Back</Link>
                </Button>
              </div>

              {isLoading ? (
                <Loader />
              ) : (
                <div>
                  {chapters?.map((object) => (
                    <Button variant="outline-dark" size="sm" key={object?.id}>
                      <Link to={`/comics/chapter/${object.id}/`}>
                        {object.name}
                      </Link>
                      <hr />
                    </Button>
                  ))}
                </div>
              )}
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
  chapters: state.comicChapters.chapters,
});

export default connect(mapStateToProps, {
  listChaptersDetails,
  listComicChapters,
})(ChaptersScreen);
