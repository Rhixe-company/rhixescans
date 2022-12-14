import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import ComicItem from "../components/content/ComicItem";
import Paginate from "../components/ui/Paginate";
import ComicsCarousel from "../components/content/ComicsCarousel";
import { listComics, listGenres } from "../actions/comicsActions";
import { Container, Row, Col } from "react-bootstrap";
import Message from "../components/ui/Message";
import { COMICS_LIST_RESET } from "../constants/comicsConstants";
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
    dispatch({ type: COMICS_LIST_RESET });
  }, [dispatch, keyword]);
  return (
    <Container>
      <Row>
        {!keyword && <ComicsCarousel />}
        <br />
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <div className="grid">
            <div>
              <b>Genres</b>
              {genres.map((genre) => (
                <Col key={genre.id}>
                  <small>{genre.name}</small>
                </Col>
              ))}
            </div>
            <div>
              <b>Lastest Comics</b>
              {comics.map((comic) => (
                <Col key={comic.id} sm={12} md={6} lg={4} xl={3}>
                  <ComicItem comic={comic} />
                </Col>
              ))}

              <Paginate page={page} pages={pages} keyword={keyword} />
            </div>
          </div>
        )}
      </Row>
    </Container>
  );
}

export default HomeScreen;
