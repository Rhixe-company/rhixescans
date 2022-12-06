import { Link } from "react-router-dom";
import { Card } from "react-bootstrap";

import Rating from "../ui/Rating";
const Comicgrid = ({ comic }) => {
  return (
    <Card className="my-3 p-3 rounded">
      <Card.Body className="px-6 py-4">
        <Link to={`/comic/${comic.id}/`}>
          <Card.Title
            as="div"
            className="font-bold text-black-500 text-xl mb-2"
          >
            <h1>{comic.title}</h1>
          </Card.Title>
        </Link>
        <Card.Img src={comic.image} alt={comic.image_url} />
        <br />
        <Card.Text as="div">
          <b>Description:</b>
          <p>{comic.description}</p>
        </Card.Text>

        <Card.Text as="div">
          <div className="my-3">
            <Rating
              value={comic.rating}
              text={` ${comic.rating} Rating`}
              color={"#f8e825"}
            />
          </div>
        </Card.Text>

        <Card.Text as="span">
          <b>Status:</b>
          {comic.status}
        </Card.Text>
        <br />
        <Card.Text as="span">
          <b>Author:</b>
          {comic.author}
        </Card.Text>
        <br />
        <Card.Text as="span">
          <b>Category:</b>
          {comic.category}
        </Card.Text>
        <br />
        <div>
          {comic.genres?.map((genre, index) => (
            <Card.Text
              as="span"
              key={index}
              className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
            >
              <strong>{genre.name}</strong>
            </Card.Text>
          ))}
        </div>
      </Card.Body>
      <hr />
      {comic.chapters?.map((chapter) => (
        <li as="span" key={chapter?.id}>
          <Link to={`/comics/chapter/${chapter.id}/`}>
            <strong>{chapter?.name}</strong>
          </Link>
          <br />
        </li>
      ))}
    </Card>
  );
};

export default Comicgrid;
