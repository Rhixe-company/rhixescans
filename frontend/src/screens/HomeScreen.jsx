import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import ComicItem from "../components/content/ComicItem";
import Paginate from "../components/ui/Paginate";
import ComicsCarousel from "../components/content/ComicsCarousel";
import { listComics, listGenres } from "../actions/comicsActions";
import { Row, Col } from "react-bootstrap";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
function HomeScreen({ history }) {
  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { comics, page, pages, error, loading } = comicsList;

  const genresList = useSelector((state) => state.genresList);
  const { genres } = genresList;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch(listComics(keyword));
    dispatch(listGenres());
  }, [dispatch, keyword]);
  return (
    <div>
      {!keyword && <ComicsCarousel />}
      <hr />
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Row>
          <h1>Lastest Comics</h1>
          {comics.map((comic) => (
            <Col key={comic.id} sm={12} md={6} lg={4} xl={3}>
              <ComicItem comic={comic} />
            </Col>
          ))}

          <Paginate page={page} pages={pages} keyword={keyword} />
          {genres.map((genre) => (
            <Col key={genre.id}>{genre.name}</Col>
          ))}
        </Row>
      )}
    </div>
  );
}

export default HomeScreen;
