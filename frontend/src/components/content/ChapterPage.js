import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Button, ListGroup, Image } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroll-component";

const ChapterPage = ({ chapter, chaptersHandler }) => {
  return (
    <div>
      <Button variant="secondary">
        <Link to={`/comic/${chapter.comics}/`}>{chapter.name}</Link>
      </Button>
      {chapter.pages?.map((page) => (
        <InfiniteScroll dataLength={page} key={page.id}>
          <Image src={page.images} alt={page.images_url} />
        </InfiniteScroll>
      ))}
      <ListGroup>
        <ListGroup.Item>
          <Button
            className="my-3"
            disabled={chapter.length === 0}
            onClick={() => chaptersHandler()}
          >
            <i className="fas fa-plus"></i> Next Chapter
          </Button>
        </ListGroup.Item>
      </ListGroup>
    </div>
  );
};

ChapterPage.propTypes = {
  chapter: PropTypes.array.isRequired,
  chapters: PropTypes.array.isRequired,
};

export default ChapterPage;
