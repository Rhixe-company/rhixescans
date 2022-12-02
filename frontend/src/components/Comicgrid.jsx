import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Image } from "react-bootstrap";
import Table from "react-bootstrap/Table";

const Comicgrid = ({ comic }) => {
  return (
    <div>
      <Table striped bordered hover size="sm" responsive="sm">
        <thead>
          <tr>
            <th>TITLE</th>
            <th>IMAGE</th>
            <th>DESCRIPTION</th>
            <th>CATEGORY</th>
            <th>RATING</th>
            <th>STATUS</th>
            <th>AUTHOR</th>
          </tr>
        </thead>
        <tbody key={comic.id}>
          <tr>
            <td>
              <Link to={`/comic/${comic.id}/`}>{comic.title}</Link>
            </td>
            <td>
              <Link to={`/comic/${comic.id}/`}>
                <Image src={comic.image} alt={comic.image_url} />
              </Link>
            </td>
            <td>{comic.description}</td>
            <td>{comic.rating}</td>
            <td>{comic.category}</td>
            <td>{comic.status}</td>
            <td>{comic.author}</td>
          </tr>
        </tbody>
      </Table>
    </div>
  );
};

Comicgrid.propTypes = {
  comic: PropTypes.array.isRequired,
};

export default Comicgrid;
