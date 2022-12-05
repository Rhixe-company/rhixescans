import { Link } from "react-router-dom";
import { Image, Row, Col } from "react-bootstrap";

import Rating from "./Rating";
const Comicgrid = ({ comic }) => {
  return (
    <Row>
      <Col>
        <Link to={`/comic/${comic.id}/`}>{comic.title}</Link>
      </Col>
      <Col>
        <Link to={`/comic/${comic.id}/`}>
          <Image src={comic.image} alt={comic.image_url} className="w-full" />
        </Link>
      </Col>
      <Col>{comic.description}</Col>
      <Col>
        <Rating
          value={comic.rating}
          text={`${comic.rating}`}
          color={"#f8e825"}
        />
      </Col>
      <Col>{comic.category}</Col>
      <Col>{comic.status}</Col>
      <Col>{comic.author}</Col>
    </Row>
  );
};

export default Comicgrid;
