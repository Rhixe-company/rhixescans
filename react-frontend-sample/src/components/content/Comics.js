import React from "react";
import { Card } from "react-bootstrap";
import Rating from "../ui/Rating";
import { Link } from "react-router-dom";

const Comics = ({ comic }) => {
  return (
    <div>
      <Card className="my-3 p-3 rounded">
        <Link to={`/comic/${comic.id}/`}>
          <Card.Img src={comic.image} />
        </Link>

        <Card.Body>
          <Card.Title as="div">
            <Link to={`/comic/${comic.id}/`}>
              <strong>{comic.title}</strong>
            </Link>
          </Card.Title>

          <Card.Text as="div">
            <div className="my-3">
              <strong>{comic.genres}</strong>
              <Rating
                value={comic.rating}
                text={`${comic.rating} `}
                color={"#f8e825"}
              />
            </div>
          </Card.Text>
        </Card.Body>
        <div>
          {comic.chapters.map((chapter) => (
            <div>
              <div key={chapter.id}>
                <ul>
                  <li>
                    <Link to={`/comic/${comic.id}/chapters/${chapter.id}`}>
                      <div className="my-3">
                        <strong>{chapter.name}</strong>
                        {chapter.number}
                      </div>
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default Comics;
