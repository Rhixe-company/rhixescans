import { Link } from "react-router-dom";
import { Image, Container, Card } from "react-bootstrap";

import Rating from "./Rating";
const Comicgrid = ({ comic, genres }) => {
  return (
    <Container>
      <Card className="my-3 p-3 rounded">
        <Card.Body className="px-6 py-4">
          <Link to={`/comic/${comic.id}/`}>
            <Image
              src={comic.image}
              alt={comic.image_url}
              width="60"
              height="60"
            />
            <Card.Title
              as="div"
              className="font-bold text-black-500 text-xl mb-2"
            >
              <b>Title:</b>
              <strong>{comic.title}</strong>
            </Card.Title>
          </Link>
          <Card.Text as="div">
            <b>Description:</b>
            <p>{comic.description}</p>
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
            <small>
              <b>Status:</b>
              {comic.status}
            </small>
          </Card.Text>
          <Card.Text as="div">
            <b>Author:</b>
            <span>{comic.author}</span>
          </Card.Text>
          <Card.Text as="div">
            <b>Category:</b>
            <span>{comic.category}</span>
          </Card.Text>

          <div>
            {genres.map((genre) => (
              <Card.Text
                as="span"
                key={genre.id}
                className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
              >
                {genre.name}
              </Card.Text>
            ))}
          </div>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Comicgrid;
