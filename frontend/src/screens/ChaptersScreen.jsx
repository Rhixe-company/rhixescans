import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listChaptersDetails } from "../actions/chaptersActions";
import { listComicChapters } from "../actions/comicsActions";

import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Link } from "react-router-dom";
import { Button, Container, Image } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroll-component";

export const ChaptersScreen = ({ history, match }) => {
  const chapterId = match.params.id;
  const dispatch = useDispatch();
  const chaptersDetails = useSelector((state) => state.chaptersDetails);
  const { chapter, error, loading } = chaptersDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const comicChapters = useSelector((state) => state.comicChapters);
  const { chapters, isLoading, isError } = comicChapters;

  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    }
    dispatch(listChaptersDetails(chapterId));
    dispatch(listComicChapters(chapter?.comics));
  }, [dispatch, history, userInfo, chapterId, chapter?.comics]);
  return (
    <div>
      {isLoading && <Loader />}
      {isError && <Message variant="danger">{isError}</Message>}
      <Button>
        <Link to={`/comic/${chapter.comics}/`}>Go Back</Link>
      </Button>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container>
          {chapter.name}

          {chapter.pages?.map((page) => (
            <InfiniteScroll dataLength={page} key={page.id}>
              <Image src={page.images} alt={page.images_url} />
            </InfiniteScroll>
          ))}
          <Link to={`/comic/${chapter.comics}/`}>
            <Button size="sm">{chapter.name}</Button>
          </Link>
          <div>
            {chapters?.map((object) => (
              <ul>
                <li key={object?.id}>
                  <Link to={`/comics/chapter/${object.id}/`}>
                    <h3>{object?.name}</h3>
                  </Link>
                </li>
              </ul>
            ))}
          </div>
        </Container>
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
