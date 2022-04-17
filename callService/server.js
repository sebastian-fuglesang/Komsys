const express = require("express");
const app = express();
const PORT = process.env.PORT || 9001;
const server = require("http").Server(app);
const { v4: uuidv4 } = require("uuid");
const io = require("socket.io")(server);

app.use(express.static("public"));
app.set('view engine', 'ejs')

app.get("/",  (req, res) => {
    res.redirect(`/${uuidv4()}`);
   })

app.get("/:room", (req, res) => {
    res.render("room", { roomId: req.params.room });
});


//MQTT Functionality
const mqtt = require("mqtt");
const host = 'mqtt.item.ntnu.no'
const port = '1883'
const clientId = `mqtt_${999}`

const connectUrl = `mqtt://${host}:${port}`
const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  reconnectPeriod: 1000,
})

const topic = 'ttm4115/team07/calls'
client.on('connect', () => {
  client.publish(topic, 'Calls', { qos: 0, retain: false }, (error) => {
    if (error) {
      console.error(error)
    }
  })
})

//Events and MQTT publish
io.on("connection", (socket) => {
    socket.on("join-room", (roomId, userId) => {
        socket.join(roomId);
        socket.broadcast.to(roomId).emit("user-connected", userId)
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