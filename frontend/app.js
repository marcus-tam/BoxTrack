// app.js
const express = require("express")
const path = require('path')
const _dirname = path.resolve(path.dirname('')); 

const app = express();

// express.static middleware is separate from res.sendFile
//app.use('/css', express.static(path.join(_dirname, 'node_modules/bootstrap/dist/css')))
//app.use('/js', express.static(path.join(_dirname, 'node_modules/bootstrap/dist/js')))
//app.use('/js', express.static(path.join(_dirname, 'node_modules/jquery/dist')))

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, 'views/example_shop.html'))
});

app.listen(5000, () => {
  console.log('Listening on port ' + 5000);
});

//node app.js to run server