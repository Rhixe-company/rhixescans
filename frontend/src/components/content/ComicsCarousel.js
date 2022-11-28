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
    <Carousel pause="hover" className="bg-dark">
      {comics.map((comic) => (
        <Carousel.Item key={comic.id}>
          <Link to={`/comic/${comic.id}`}>
            <Image
              className="comics-img"
              src={comic.image}
              alt={comic.image}
              fluid
            />
            <Carousel.Caption className="carousel.caption">
              <span>{comic.title}</span>
            </Carousel.Caption>
          </Link>
        </Carousel.Item>
      ))}
    </Carousel>
  );
};

export default ComicsCarousel;
