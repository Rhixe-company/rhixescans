import axios from "axios";

// Create new comic
const createComic = async (comicData, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const response = await axios.post("/api/comics/create/", comicData, config);
  return response.data;
};

// Get comics
const getComics = async (token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const response = await axios.get("/api/comics/", config);
  return response.data;
};

// Delete comic
const deleteComic = async (id, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const response = await axios.delete("/api/comics/delete/" + id, config);
  return response.data;
};

const comicService = {
  createComic,
  getComics,
  deleteComic,
};

export default comicService;
