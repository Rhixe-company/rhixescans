import React from "react";
import Rating from "../ui/Rating";
import { Link } from "react-router-dom";
import { Card } from "react-bootstrap";
import { Container } from "react-bootstrap";
const ComicItem = ({ comic }) => {
  return (
    <Container className="max-w-sm rounded overflow-hidden shadow-lg">
      <Card className="my-3 p-3 rounded">
        <Card.Body className="px-6 py-4">
          <Link to={`/comic/${comic.id}/`}>
            <Card.Img
              fluid="true"
              className="w-full"
              src={comic.image}
              alt={comic.image_url}
            />
          </Link>
          <Link className="px-6 py-4" to={`/comic/${comic.id}/`}>
            <Card.Title className="font-bold text-purple-500 text-xl" as="div">
              {comic.title}
            </Card.Title>
          </Link>
          <Card.Text as="ul">
            <li>
              <Rating
                value={comic.rating}
                text={` ${comic.rating} `}
                color={"#f8e825"}
              />
            </li>
            <li>
              <strong>Status:</strong>
              {comic.status}
            </li>
            <li>
              <strong>Category:</strong>
              {comic.category}
            </li>
          </Card.Text>

          <div className="px-6 py-4">
            {comic.genres?.map((genre) => (
              <Card.Text
                className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
                as="span"
                key={genre.id}
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

export default ComicItem;
