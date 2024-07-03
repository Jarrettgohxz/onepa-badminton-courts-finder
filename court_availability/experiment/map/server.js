const http = require("http");
const fs = require("fs");
const url = require("url");

const server = http.createServer((req, res) => {
  const path = url.parse(req.url).pathname;

  switch (path) {
    case "/":
      res.writeHead(200, { "content-type": "text/html" });
      fs.createReadStream("map.html").pipe(res);
      break;

    case "/map.js":
    case "/env.js": {
      fs.readFile(__dirname + path, (error, data) => {
        if (error) {
          res.writeHead(404);
          res.write(error);
          res.end();

          //
        } else {
          res.writeHead(200, { "Content-Type": "text/html" });
          res.write(data);
          res.end();
        }
      });

      break;
    }

    case "/favicon.ico":
      res.end();
      break;

    default:
      break;
  }
});

const PORT = 4000;

server.listen(PORT, () => console.log(`Server listening on port ${PORT}...`));
