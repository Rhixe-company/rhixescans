import React from "react";
import Rating from "../ui/Rating";
import { Link } from "react-router-dom";
import { Container } from "react-bootstrap";
const ComicItem = ({ comic }) => {
  const genres = comic.genres;
  return (
    <Container>
      <div className="max-w-sm rounded overflow-hidden shadow-lg">
        <Link to={`/comic/${comic.id}/`}>
          <img
            fluid="true"
            className="w-full"
            src={comic.image}
            alt={comic.image_url}
          />
        </Link>
        <div className="px-6 py-4">
          <Link to={`/comic/${comic.id}/`}>
            <div className="font-bold text-purple-500 text-xl mb-2">
              {comic.title}
            </div>
          </Link>

          <ul>
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
          </ul>

          {genres.map((genre, index) => (
            <span
              key={index}
              className="inline-block  bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
            >
              {genre.name}
            </span>
          ))}
        </div>
      </div>
    </Container>
  );
};

export default ComicItem;
