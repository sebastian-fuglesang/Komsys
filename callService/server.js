const express = require("express");
const app = express();
const PORT = process.env.PORT || 3002;
const { v4: uuidv4 } = require("uuid");
const server = require("http").Server(app);
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
  console.log('Connected')
  client.subscribe([topic], () => {
    console.log(`Subscribe to topic '${topic}'`)
  })
  client.publish(topic, 'Calls', { qos: 0, retain: false }, (error) => {
    if (error) {
      console.error(error)
    }
  })
})
client.on('message', (topic, payload) => {
  console.log('Received Message:', topic, payload.toString())
})



app.use(express.static("public"));
app.set('view engine', 'ejs')

app.get("/",  (req, res) => {
    res.redirect(`/${uuidv4()}`);
   })

app.get("/:room", (req, res) => {
    res.render("room", { roomId: req.params.room });
});

const io = require("socket.io")(server, {
    allowEIO3: true
});
const { ExpressPeerServer } = require("peer");
const peerServer = ExpressPeerServer(server, {
debug: true,
});
app.use("/peerjs", peerServer);

io.on("connection", (socket) => {
    socket.on("join-room", (roomId, userId) => {
        socket.join(roomId);
        socket.to(roomId).broadcast.emit("user-connected", userId);
        client.publish(topic, roomId,)
        socket.on('messageSent', (text, userId) => {
            //socket.to(roomId).emit('messageReceived', msg);
            io.sockets.in(roomId).emit("messageReceived", text, userId)
          });
        socket.on('disconnect', () => {
            socket.to(roomId).broadcast.emit('user-disconnected', userId)
          })
    });
});

server.listen(PORT);

