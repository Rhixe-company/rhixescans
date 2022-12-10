import { Link } from "react-router-dom";
import { Container, Card, Image } from "react-bootstrap";

import Rating from "../ui/Rating";
const Comicgrid = ({ comic }) => {
  return (
    <Container key={comic.id}>
      <Card className="my-3 p-3 rounded">
        <Card.Body className="px-6 py-4">
          <Link to={`/comic/${comic.id}/`}>
            <Card.Title as="div">
              <h2 className="font-bold text-black-500 text-xl mb-2">
                {comic.title}
              </h2>
            </Card.Title>
          </Link>
          <br />
          <Link to={`/comic/${comic.id}/`}>
            <Image
              fluid="true"
              className="d-block w-100"
              src={comic.image}
              alt={comic.image_url}
            />
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
          </Card.Text>

          <Card.Text as="div">
            <b>Status:</b>
            {comic.status}
          </Card.Text>

          <Card.Text as="div">
            <b>Author:</b>
            {comic.author}
          </Card.Text>

          <Card.Text as="div">
            <b>Category:</b>
            <strong>{comic.category}</strong>
          </Card.Text>

          <Card.Text as="div">
            <b>Release Date:</b>
            {new Date(comic.created).toLocaleString("en-US")}
          </Card.Text>

          <Card.Text as="div">
            <b>Last Updated:</b>
            {new Date(comic.updated).toLocaleString("en-US")}
          </Card.Text>
          <br />
          <h4>Genres:</h4>
          <br />
          {comic.genres?.map((genre, index) => (
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
    </Container>
  );
};

export default Comicgrid;
