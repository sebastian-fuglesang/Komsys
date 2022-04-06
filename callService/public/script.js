const socket = io();
const videoGrid = document.getElementById("video-grid");
const myVideo = document.createElement("video");
myVideo.muted = true;

const peers = {}

var myPeer = new Peer(undefined, {
    path: "/peerjs",
    host: "/",
    port: "",
});

let myVideoStream;
navigator.mediaDevices
    .getUserMedia({
        audio: true,
        video: true,
    })
    .then((stream) => {
        myVideoStream = stream;
        addVideoStream(myVideo, stream);
        myPeer.on("call", (call) => {
            console.log("call initiated")
            call.answer(stream);
            const video = document.createElement("video");
            call.on("stream", (userVideoStream) => {
            addVideoStream(video, userVideoStream);
            });
        });
        socket.on("user-connected", (userId) => {
            console.log("user with userId " + userId + " connected.")
            connectToNewUser(userId, stream);
            });
        });


myPeer.on("open", (id) => {
    socket.emit("join-room", ROOM_ID, id);
    console.log("you have the following roomId " + ROOM_ID)
});

socket.on('user-disconnected', userId => {
    console.log("user with userId " + userId + " disconnected.")
    if (peers[userId]) peers[userId].close()
  })

function addVideoStream(video, stream) {
    video.srcObject = stream;
    video.addEventListener("loadedmetadata", () => {
    video.play();
    });
    videoGrid.append(video);
};

function connectToNewUser(userId, stream) {
    const call = myPeer.call(userId, stream);
    const video = document.createElement("video");
    call.on("stream", (userVideoStream) => {
        addVideoStream(video, userVideoStream);
    });

    call.on('close', () => {
        console.log("call closed and video should be removed")
        video.remove()
      })
      peers[userId] = call
};

  //Chat stuff

  var form = document.querySelector('form');
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var input = document.querySelector('#message-input');
    var text = input.value;
    socket.emit('messageSent', text);
    input.value = '';
  });
  
socket.on('messageReceived', text => {
    console.log("message received")
    receiveNewMessage(text)
});

function receiveNewMessage(newMessageContent) {
    if (!newMessageContent){
      return;
    }
    console.log(newMessageContent)
      
    var chatMessageContainer = document.getElementById("chat-message-container");
    var newMessage = document.createElement("p");
    newMessage.innerText = newMessageContent;
    chatMessageContainer.appendChild(newMessage);
    var seperator = document.createElement('br');
    chatMessageContainer.appendChild(seperator);
    }
      