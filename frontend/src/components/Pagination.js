import React from "react";
import { LinkContainer } from "react-router-bootstrap";

const Pagination = ({ postsPerPage, totalPosts, paginate, chapterId }) => {
  const pageNumbers = [];
  for (let i = 1; i <= Math.ceil(totalPosts / postsPerPage); i++) {
    pageNumbers.push(i);
  }
  return (
    <nav>
      <ul className="pagination">
        {pageNumbers.map((number) => (
          <li key={number} className="page-item">
            <LinkContainer
              onClick={() => paginate(number)}
              to={`#/comics/chapter/${chapterId}`}
              className="page-link"
            >
              {number}
            </LinkContainer>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Pagination;
