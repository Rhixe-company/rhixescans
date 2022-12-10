import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Rating from "../components/ui/Rating";
import { Link } from "react-router-dom";
import { Card, Container, Image } from "react-bootstrap";
import Paginate from "../components/ui/Paginate";
import ComicsCarousel from "../components/content/ComicsCarousel";
import { listComics } from "../actions/comicsActions";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";

function HomeScreen({ history }) {
  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { comics, page, pages, comics_count, error, loading } = comicsList;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch(listComics(keyword));
  }, [dispatch, keyword]);
  return (
    <Container className="container mx-auto">
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <div>
          {!keyword && <ComicsCarousel />}
          <br />
          <strong>{comics_count} comics available</strong>
          {comics.map((comic) => (
            <div key={comic.id}>
              <Card className="my-3 p-3 rounded">
                <Card.Body className="px-6 py-4">
                  <Link to={`/comic/${comic.id}/`}>
                    <Image
                      width="300"
                      height="300"
                      src={comic.image}
                      alt={comic.image_url}
                    />
                  </Link>
                  <Link to={`/comic/${comic.id}/`}>
                    <Card.Title as="div">
                      <h2 className="font-bold text-black-500 text-xl mb-2">
                        {comic.title}
                      </h2>
                    </Card.Title>
                  </Link>

                  <Card.Text as="div">
                    <b>Status:</b>
                    {comic.status}
                  </Card.Text>

                  <Card.Text as="div">
                    <div className="my-3">
                      <b>Rating:</b>

                      <Rating
                        value={comic.rating}
                        text={` ${comic.rating} `}
                        color={"#f8e825"}
                      />
                    </div>
                  </Card.Text>

                  <Card.Text as="div">
                    <div>
                      <b>Last Updated:</b>
                      {new Date(comic.updated).toLocaleString("en-US")}
                    </div>
                    <br />
                    <div>
                      <b>Author:</b>
                      {comic.author}
                    </div>
                  </Card.Text>
                </Card.Body>

                <Card.Text as="div">
                  <br />
                  <div>
                    <b>Tags:</b>
                    <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2">
                      {comic.category}
                    </span>
                  </div>
                </Card.Text>
              </Card>
            </div>
          ))}

          <Paginate page={page} pages={pages} keyword={keyword} />
        </div>
      )}
    </Container>
  );
}

export default HomeScreen;
