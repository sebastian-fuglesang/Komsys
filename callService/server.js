//Seting up the epress js server
const express = require("express");
const app = express();
const PORT = process.env.PORT || 9001;
const server = require("http").Server(app);
const { v4: uuidv4 } = require("uuid");
const io = require("socket.io")(server);

app.use(express.static("public"));
app.set('view engine', 'ejs')

//Redirect users going to the root route to a randomly generated roomId
app.get("/",  (req, res) => {
    res.redirect(`/${uuidv4()}`);
   })

app.get("/:room", (req, res) => {
    res.render("room", { roomId: req.params.room });
});


//MQTT Functionality

//Setup of MQTT 
const mqtt = require("mqtt");
const host = 'mqtt.item.ntnu.no'
const port = '1883'
const clientId = `mqtt_${999}`
const topic = 'ttm4115/team07/calls'

const connectUrl = `mqtt://${host}:${port}`
const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  reconnectPeriod: 1000,
})

//Events and MQTT publish
io.on("connection", (socket) => {
    socket.on("join-room", (roomId, userId) => {
        socket.join(roomId);
        socket.broadcast.to(roomId).emit("user-connected", userId)
        //When a user connects to a room publish the roomId they connected to in the chosen topic
        client.publish(topic, roomId)
        socket.on('messageSent', (text, userId) => {
            io.sockets.in(roomId).emit("messageReceived", text, userId)
          });
        socket.on('disconnect', () => {
            io.sockets.in(roomId).emit('user-disconnected', userId)
          })
    });
});

server.listen(PORT)