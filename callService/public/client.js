const socket = io();
const videoGrid = document.getElementById("video-grid");
const myVideo = document.createElement("video");
myVideo.muted = true;
var myUserId = "";
const peers = {}

//Videocall functionality
let myVideoStream;
navigator.mediaDevices
    .getUserMedia({
        audio: true,
        video: true,
    })
    .then((stream) => {
        const myPeer = new Peer(undefined, {
            host: "ttm4115-peerjs-server.herokuapp.com",
            port: 443,
            secure: true,
            path: "/"
        });

        function connectToNewUser(userId, stream) {
            const call = myPeer.call(userId, stream, {metadata : {"caller_id": myUserId}});
            const video = document.createElement("video");
            call.on("stream", (userVideoStream) => {
                addVideoStream(video, userVideoStream, userId);
            });
            peers[userId] = call
        };

        myPeer.on("open", (id) => {
            socket.emit("join-room", ROOM_ID, id);
            myUserId = id;
        });
        myVideoStream = stream;
        addVideoStream(myVideo, stream);
        myPeer.on("call", (call) => {
            call.answer(stream);
            const video = document.createElement("video");
            call.on("stream", (userVideoStream) => {
                addVideoStream(video, userVideoStream, call.metadata.caller_id);
            });
            call.on("error", () => {
                console.log("error")
            })
        });

        socket.on("user-connected", (userId) => {
            connectToNewUser(userId, stream);
            });
        });


socket.on('user-disconnected', userId => {
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
    videoGrid.append(video);
};


function removeVideoWithUserId(userId) {
    if (document.getElementById(userId) != null) {
        document.getElementById(userId).remove();
    }
}

 //Chat Functionality
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
