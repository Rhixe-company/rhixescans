import React from "react";
import { Link } from "react-router-dom";

const ChaptersGrid = ({ chapters }) => {
  return (
    <div>
      {chapters?.map((object) => (
        <ul key={object.id}>
          <li>
            <Link to={`/comics/chapter/${object.id}/`}>
              <h3>{object.name}</h3>
            </Link>
          </li>
        </ul>
      ))}
    </div>
  );
};

export default ChaptersGrid;
