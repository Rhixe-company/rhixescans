import React from "react";
import Rating from "../ui/Rating";
import { Link } from "react-router-dom";
import { Card } from "react-bootstrap";
const ComicItem = ({ comic }) => {
  return (
    <div>
      <Card className="my-3 p-3 rounded">
        <Card.Body className="px-6 py-4">
          <Link to={`/comic/${comic.id}/`}>
            <Card.Title
              className="font-bold text-black-500 text-xl mb-2"
              as="div"
            >
              <h3>{comic.title}</h3>
            </Card.Title>
          </Link>

          <Card.Text as="div">
            <Link to={`/comic/${comic.id}/`}>
              <Card.Img
                fluid="true"
                className="d-block w-70"
                src={comic.image}
                alt={comic.image}
              />
            </Link>
            <div className="my-3">
              <Rating
                value={comic.rating}
                text={` ${comic.rating} `}
                color={"#f8e825"}
              />
              <br />
              <b>Release Date:</b>
              {comic.release_date}
            </div>
          </Card.Text>
          <Card.Text as="div">
            <div className="my-3">
              <b>Status:</b>
              {comic.status}
            </div>
          </Card.Text>

          <Card.Text as="div">
            <div className="my-3">
              <b>Category:</b>
              {comic.category}
            </div>
          </Card.Text>

          <Card.Text as="div">
            <div className="my-3">
              <b>Updated:</b>
              {new Date(comic.updated).toLocaleString("en-US")}
            </div>
          </Card.Text>

          {comic.genres?.map((genre) => (
            <Card.Text
              as="div"
              key={genre.id}
              className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
            >
              <span>{genre.name}</span>
            </Card.Text>
          ))}
        </Card.Body>
      </Card>
    </div>
  );
};

export default ComicItem;
