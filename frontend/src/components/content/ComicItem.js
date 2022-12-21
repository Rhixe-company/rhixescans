import React from "react";
import { Card } from "react-bootstrap";
import Rating from "../ui/Rating";
import { Link } from "react-router-dom";
const ComicItem = ({ comic }) => {
  const genres = comic.genres;
  return (
    <Card className="my-3 p-3 rounded">
      <Link to={`/comic/${comic.id}/`}>
        <Card.Img src={comic.image} />
      </Link>
      <Card.Body>
        <Link to={`/comic/${comic.id}/`}>
          <Card.Title as="div">
            <strong>{comic.title}</strong>
          </Card.Title>
        </Link>

        <Card.Text>
          <div className="my-3">
            <Rating
              value={comic.rating}
              text={` ${comic.rating} `}
              color={"#f8e825"}
            />
          </div>
        </Card.Text>
        <Card.Text>
          <b>Last Updated:</b>
          {new Date(comic.updated).toLocaleString("en-us")}
        </Card.Text>
        <Card.Text>
          <b>Artist:</b>
          {comic.artist}
        </Card.Text>
        <Card.Text>
          <b>Status:</b>
          {comic.status}
        </Card.Text>
        <Card.Text>
          <b>Category:</b>
          {comic.category}
        </Card.Text>

        {genres.map((genre, index) => (
          <Card.Text
            as="span"
            key={index}
            className="inline-block  bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
          >
            {genre.name}
          </Card.Text>
        ))}
      </Card.Body>
    </Card>
  );
};

export default ComicItem;
