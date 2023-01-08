import React from "react";

const Chapter = ({ chapter }) => {
  return (
    <ul>
      <li>
        <div>{chapter?.name}</div>
      </li>
    </ul>
  );
};

export default Chapter;
