const feedDisplay = document.querySelector("#load");

fetch("http://localhost:8000/api/comics/crawl")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
  })
  .catch((err) => console.log(err));
