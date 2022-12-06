import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Rating from "../components/ui/Rating";
import { Link } from "react-router-dom";
import { Card, Container } from "react-bootstrap";
import Paginate from "../components/ui/Paginate";
import ComicsCarousel from "../components/content/ComicsCarousel";
import { listComics } from "../actions/comicsActions";

function HomeScreen({ history }) {
  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { comics, page, pages } = comicsList;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch(listComics(keyword));
  }, [dispatch, keyword]);
  return (
    <Container className="container mx-auto">
      {!keyword && <ComicsCarousel />}
      <br />
      <h1>Latest Comics</h1>
      <div>
        {comics.map((comic) => (
          <div key={comic.id}>
            <Card className="my-3 p-3 rounded">
              <Card.Body className="px-6 py-4">
                <Link to={`/comic/${comic.id}/`}>
                  <Card.Title
                    as="div"
                    className="font-bold text-black-500 text-xl mb-2"
                  >
                    <strong>{comic.title}</strong>
                  </Card.Title>
                  <Card.Img src={comic.image} alt={comic.image_url} />
                </Link>
                <small>
                  <b>Status:</b>
                  {comic.status}
                </small>
                <Card.Text as="div">
                  <div className="my-3">
                    <b>Rating:</b>

                    <Rating
                      value={comic.rating}
                      text={` ${comic.rating} `}
                      color={"#f8e825"}
                    />
                  </div>
                  <p>
                    <b>Author:</b>
                    {comic.author}
                  </p>
                </Card.Text>

                <Card.Text as="div">
                  <b>Category:</b>
                  <strong>{comic.category}</strong>
                </Card.Text>
                <br />
                {comic.genres.map((genre, index) => (
                  <Card.Text
                    as="span"
                    key={index}
                    className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
                  >
                    <strong>{genre.name}</strong>
                  </Card.Text>
                ))}
              </Card.Body>
            </Card>
          </div>
        ))}

        <Paginate page={page} pages={pages} keyword={keyword} />
      </div>
    </Container>
  );
}

export default HomeScreen;
