import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import ComicItem from "../components/content/ComicItem";
import Paginate from "../components/ui/Paginate";
import ComicsCarousel from "../components/content/ComicsCarousel";
import { listComics } from "../actions/comicsActions";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Container } from "react-bootstrap";
function HomeScreen({ history }) {
  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { comics, page, pages, comics_count, error, loading } = comicsList;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch(listComics(keyword));
  }, [dispatch, keyword]);
  return (
    <section>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container className="container mx-auto">
          <section>
            {!keyword && <ComicsCarousel />}
            <h3>Recent Comics</h3>
            {comics.map((comic) => (
              <div key={comic.id}>
                <ComicItem comic={comic} />
              </div>
            ))}
          </section>

          <Paginate page={page} pages={pages} keyword={keyword} />
          <b>{comics_count} comics available</b>
        </Container>
      )}
    </section>
  );
}

export default HomeScreen;
