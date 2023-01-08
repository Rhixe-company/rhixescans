import React from "react";
import PropTypes from "prop-types";

import { Image } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroll-component";

const ChapterPage = ({ chapter }) => {
  return (
    <div>
      {chapter.pages?.map((page) => (
        <InfiniteScroll dataLength={page} key={page.id}>
          <Image src={page.images} alt={page.images_url} />
        </InfiniteScroll>
      ))}
    </div>
  );
};

ChapterPage.propTypes = {
  chapter: PropTypes.array.isRequired,
};

export default ChapterPage;
