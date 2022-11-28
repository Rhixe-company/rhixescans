import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Button, Image } from "react-bootstrap";
import Loader from "../components/ui/Loader";
import Message from "../components/ui/Message";
const ChapterScreen = ({ match }) => {
  const [chapter, setChapter] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(true);
  useEffect(() => {
    fetch(`api/chapters/${match.params.id}/`)
      .then((res) => res.json())
      .then((data) => {
        setChapter(data);
        setIsLoading(false);
        setError(false);
      })
      .catch((err) => console.log(err));
  }, [match]);

  return (
    <div>
      <Link to="/">
        <Button>Go Back </Button>
      </Link>
      {!isLoading && chapter.length === 0 && <small>Pages Not Found</small>}
      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <div>
          <div>
            <Link to={`/comics/chapter/${chapter.id}/`}>
              <h3>{chapter.name}</h3>
            </Link>
          </div>
          <div>
            {chapter.pages.map((page, index) => (
              <span key={index}>
                <Image
                  className="w-full"
                  src={page?.images}
                  alt={page?.images_url}
                />
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChapterScreen;
