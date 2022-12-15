import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Button, Image } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroll-component";

const ChapterPage = ({ chapter }) => {
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
      <Link to={`/comic/${chapter.comics}/`}>
        <Button variant="secondary">{chapter.name}</Button>
      </Link>
    </div>
  );
};

ChapterPage.propTypes = {
  chapter: PropTypes.array.isRequired,
};

export default ChapterPage;
