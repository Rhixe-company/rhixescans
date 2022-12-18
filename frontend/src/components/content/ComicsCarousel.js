import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { Carousel, Image } from "react-bootstrap";
import Loader from "../ui/Loader";
import Message from "../ui/Message";
import { listTopComics } from "../../actions/comicsActions";

const ComicsCarousel = () => {
  const dispatch = useDispatch();

  const comicsTopRated = useSelector((state) => state.comicsTopRated);
  const { error, loading, comics } = comicsTopRated;

  useEffect(() => {
    dispatch(listTopComics());
  }, [dispatch]);
  return loading ? (
    <Loader />
  ) : error ? (
    <Message variant="danger">{error}</Message>
  ) : (
    <section>
      <h3>Top Comics</h3>
      <Carousel fade variant="dark" className="bg-dark">
        {comics.map((comic) => (
          <Carousel.Item interval={2000} key={comic.id}>
            <Link to={`/comic/${comic.id}`}>
              <Image
                className="d-block w-100"
                src={comic.image}
                alt={comic.image_url}
                fuild="true"
              />
              <Carousel.Caption className="carousel.caption">
                <h4>{comic.title}</h4>
              </Carousel.Caption>
            </Link>
          </Carousel.Item>
        ))}
      </Carousel>
    </section>
  );
};

export default ComicsCarousel;
