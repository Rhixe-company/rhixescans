import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listChaptersDetails } from "../actions/chaptersActions";
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
  useEffect(() => {
    dispatch(listChaptersDetails(chapterId));
  }, [dispatch, chapterId]);
  return (
    <Container>
      <div>
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <div>
            {userInfo ? (
              <div>
                <Link to={`/comic/${chapter.comics}/`}>
                  <Button>Go Back</Button>
                </Link>
                <div>
                  <Link to={`/comics/chapter/${chapter.id}/`}>
                    <h1>{chapter.name}</h1>
                  </Link>
                </div>
                <div>
                  {chapter.pages?.map((page, index) => (
                    <div className="pages" key={index}>
                      <InfiniteScroll dataLength={page} className="pages">
                        <Image
                          className="page"
                          src={page?.images}
                          alt={page?.images_url}
                        />
                      </InfiniteScroll>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <Link to="/login">
                <Button>Please Login To Read Comic</Button>
              </Link>
            )}
          </div>
        )}
      </div>
    </Container>
  );
};

const mapStateToProps = (state) => ({
  chapter: state.chaptersDetails.chapter,
});

export default connect(mapStateToProps, { listChaptersDetails })(
  ChaptersScreen
);
