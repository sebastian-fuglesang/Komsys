const socket = io();
const videoGrid = document.getElementById("video-grid");
const myVideo = document.createElement("video");
myVideo.muted = true;
var myUserId = "";

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
            console.log(call)
            console.log(call.metadata.caller_id)
            call.answer(stream);
            const video = document.createElement("video");
            call.on("stream", (userVideoStream) => {
            addVideoStream(video, userVideoStream, call.metadata.caller_id);
            });

            call.on('close', () => {
                console.log("initiating user disconnected and call should now be removed")
                video.remove()
              })

            call.on("error", () => {
                console.log("error")
            })
        });
        socket.on("user-connected", (userId) => {
            console.log("user with userId " + userId + " connected.")
            connectToNewUser(userId, stream);
            console.log(peers)
            });
        });


myPeer.on("open", (id) => {
    socket.emit("join-room", ROOM_ID, id);
    console.log("setting my user id to " + id);
    myUserId = id;
});

socket.on('user-disconnected', userId => {
    console.log("user with userId " + userId + " disconnected.");
    removeVideoWithUserId(userId);
    if (peers[userId]) {
        peers[userId].close();
        removeVideoWithUserId(userId);
    }
  })

function addVideoStream(video, stream, userId) {
    video.srcObject = stream;
    video.setAttribute("id", userId)
    video.addEventListener("loadedmetadata", () => {
    video.play();
    });
    isVideoStillStreaming(video)
    videoGrid.append(video);
};

function connectToNewUser(userId, stream) {
    const call = myPeer.call(userId, stream, {metadata : {"caller_id": myUserId}});
    const video = document.createElement("video");
    call.on("stream", (userVideoStream) => {
        addVideoStream(video, userVideoStream, userId);
    });

    call.on('close', () => {
        //video.remove()
      })
    peers[userId] = call
};

function removeVideoWithUserId(userId) {
    if (document.getElementById(userId) != null) {
        document.getElementById(userId).remove();
    }
}

function isVideoStillStreaming(video) {
    video.addEventListener("ended", () => {
        console.log("video ended")
    })
}

  //Chat stuff

  var form = document.querySelector('form');
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var input = document.querySelector('#message-input');
    var text = input.value;
    socket.emit('messageSent', text, myUserId);
    input.value = '';
  });
  
socket.on('messageReceived', (text, userId) => {
    receiveNewMessage(text, userId)
});

function receiveNewMessage(newMessageContent, userId) {
    if (!newMessageContent){
      return;
    }      
    var chatMessageContainer = document.getElementById("chat-message-container");
    var messageForm = document.getElementById("message-form")
    var newMessage = document.createElement("p");
    newMessage.classList.add("message")
    newMessage.innerText = newMessageContent;
    if (userId === myUserId) {
        newMessage.classList.add("own-message")
    }
    else {
        newMessage.classList.add("others-message")
    }
    chatMessageContainer.appendChild(newMessage);
    var seperator = document.createElement('br');
    chatMessageContainer.appendChild(seperator);
    }
      