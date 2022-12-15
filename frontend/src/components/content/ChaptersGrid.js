import React from "react";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import PropTypes from "prop-types";
const ChaptersGrid = ({ chapters }) => {
  return (
    <div>
      {chapters?.map((object) => (
        <ListGroup key={object.id}>
          <ListGroup.Item>
            <Link to={`/comics/chapter/${object.id}/`}>
              <span>{object.name}</span>
            </Link>
          </ListGroup.Item>
        </ListGroup>
      ))}
    </div>
  );
};
ChaptersGrid.propTypes = {
  chapters: PropTypes.array.isRequired,
};
export default ChaptersGrid;
