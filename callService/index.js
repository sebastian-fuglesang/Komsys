const PORT = process.env.PORT || 5000;
const express = require('express');
const app = express();
const http = require('http');
const server = http.Server(app);
const io = require('socket.io')(server);

app.set("view engine", "ejs");
app.use(express.static('client'));


server.listen(PORT, function() {
  console.log('Chat server running');
});

app.get("/", (req, res) => {
  res.redirect("/test");
})

app.get("/test", (req, res) => {
  res.render("index.html")

})

io.on('connection', function(socket) {
  socket.broadcast.emit("user-connected", "Hei hei fra meg")
  socket.on('message', function(msg) {
    io.emit('message', msg);
  });


});
