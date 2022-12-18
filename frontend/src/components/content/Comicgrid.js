import { Link } from "react-router-dom";
import { ListGroup, Card, Button } from "react-bootstrap";
import Loader from "../ui/Loader";
import Rating from "../ui/Rating";
const Comicgrid = ({ comic, chapters }) => {
  return (
    <Card key={comic.id} className="my-3 p-3 rounded">
      <Link to="/">
        <Button>Go Back</Button>
      </Link>
      <Card.Body className="px-6 py-4">
        <Link to={`/comic/${comic.id}/`}>
          <Card.Title as="div">
            <h2 className="font-bold text-black-500 text-xl mb-2">
              {comic.title}
            </h2>
          </Card.Title>
        </Link>
        <Card.Text as="div">
          <Link to={`/comic/${comic.id}/`}>
            <Card.Img
              fluid="true"
              className="d-block w-50"
              src={comic.image}
              alt={comic.image}
            />
          </Link>
          <div className="my-3">
            <b>Rating:</b>

            <Rating
              value={comic.rating}
              text={` ${comic.rating} `}
              color={"#f8e825"}
            />
          </div>
        </Card.Text>

        <Card.Text as="div">
          Description:
          <p>{comic.description}</p>
        </Card.Text>

        <Card.Text as="div">
          <b>Status:</b>
          {comic.status}
        </Card.Text>

        <Card.Text as="div">
          <div className="my-3">
            <b>Artist:</b>
            {comic.artist}
          </div>
        </Card.Text>
        <Card.Text as="div">
          <div className="my-3">
            <b>Author:</b>
            {comic.author}
          </div>
        </Card.Text>

        <Card.Text as="div">
          <b>Category:</b>
          <span>{comic.category}</span>
        </Card.Text>
        <Card.Text as="div">
          <div className="my-3">
            <b>Release Date:</b>
            {comic.release_date}
          </div>
        </Card.Text>

        <Card.Text as="div">
          <b>Last Updated:</b>
          {new Date(comic.updated).toLocaleString("en-US")}
        </Card.Text>

        {comic.genres?.map((genre) => (
          <Card.Text
            as="div"
            key={genre.id}
            className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
          >
            <span>{genre.name}</span>
          </Card.Text>
        ))}
      </Card.Body>
      <br />
      {chapters?.length > 0 ? (
        <div>
          <b>Total Chapters: {comic.numChapters}</b>

          {chapters?.map((chapter) => (
            <ListGroup key={chapter.id}>
              <ListGroup.Item>
                <Link to={`/comics/chapter/${chapter.id}/`}>
                  <span>{chapter.name}</span>
                </Link>
              </ListGroup.Item>
            </ListGroup>
          ))}
        </div>
      ) : (
        <div>
          loading ...
          <Loader />
        </div>
      )}
    </Card>
  );
};

export default Comicgrid;
