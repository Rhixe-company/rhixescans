import { Link } from "react-router-dom";

import { ListGroup } from "react-bootstrap";
const PagesPagination = ({ chapter }) => {
  return (
    <div className="container mx-auto">
      <ListGroup>
        <ListGroup.Item>
          <Link to={`/comics/chapter/${chapter.id}/`}>
            <span>{chapter.name}</span>
          </Link>
        </ListGroup.Item>
      </ListGroup>
    </div>
  );
};

export default PagesPagination;
