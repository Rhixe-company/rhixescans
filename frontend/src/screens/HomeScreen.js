import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Row, Col } from "react-bootstrap";
import Comics from "../components/content/Comics";
import Loader from "../components/ui/Loader";
import Message from "../components/ui/Message";
import Paginate from "../components/ui/Paginate";
import ComicsCarousel from "../components/content/ComicsCarousel";

import { listComics } from "../actions/comicsActions";
import { listChapters } from "../actions/chaptersActions";

const HomeScreen = ({ history }) => {
  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { error, loading, comics, page, pages } = comicsList;
  const chaptersList = useSelector((state) => state.chaptersList);
  const { chapters } = chaptersList;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch(listComics(keyword));
    dispatch(listChapters());
  }, [dispatch, keyword]);

  return (
    <div>
      <div>
        <div>
          {!keyword && <ComicsCarousel />}

          <h1>Latest Comics</h1>
          {loading ? (
            <Loader />
          ) : error ? (
            <Message variant="danger">{error}</Message>
          ) : (
            <div>
              <Row>
                {comics.map((comic) => (
                  <Col key={comic.id} sm={12} md={6} lg={4} xl={3}>
                    <Comics chapters={chapters} comic={comic} />
                  </Col>
                ))}
              </Row>
              <Paginate page={page} pages={pages} keyword={keyword} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;
