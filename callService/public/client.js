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
        //Uses the PeerJs server created with the template from Heroku. Did this as there was several issues
        //when attempting to have the peerJs server defined within the server.js file.
        const myPeer = new Peer(undefined, {
            host: "ttm4115-peerjs-server.herokuapp.com",
            port: 443,
            secure: true,
            path: "/"
        });

        //Function to connect to a new user using your own video stream and the new users userId.
        //Performs a peerjs call to the provided userId. Called by the clients already in the room when a new client joins.
        function connectToNewUser(userId, stream) {
            const call = myPeer.call(userId, stream, {metadata : {"caller_id": myUserId}});
            const video = document.createElement("video");
            call.on("stream", (userVideoStream) => {
                addVideoStream(video, userVideoStream, userId);
            });
            peers[userId] = call
        };

        //Fire the join-room event to the server so the server can broadcast it to the other users in the room.
        myPeer.on("open", (id) => {
            socket.emit("join-room", ROOM_ID, id);
            myUserId = id;
        });
        myVideoStream = stream;
        addVideoStream(myVideo, stream);

        //Answer the call made by other users. This is used by the joining client to answer the calls made by the
        //clients already in the room. 
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

//Function to add a new video to the video grid. It uses the new user's userId as the id of the video in order to control
//the removal of the videos.
function addVideoStream(video, stream, userId) {
    video.srcObject = stream;
    video.setAttribute("id", userId)
    video.addEventListener("loadedmetadata", () => {
        video.play();
    });
    videoGrid.append(video);
};

//Function to remove a user with a given userId. If the client has a video with the given user id then remove it.
//This was needed as the close event from peerjs didnt fire propperly if users just closed the window.
function removeVideoWithUserId(userId) {
    if (document.getElementById(userId) != null) {
        document.getElementById(userId).remove();
    }
}

 //Chat Functionality

 //Functionality for sending messages.
 const form = document.querySelector('form');
 form.addEventListener('submit', function(e) {
   e.preventDefault();
   const input = document.querySelector('#message-input');
   const text = input.value;
   socket.emit('messageSent', text, myUserId);
   input.value = '';
 });
 
 //Listen to the server sending out messages sent by users.
socket.on('messageReceived', (text, userId) => {
    receiveNewMessage(text, userId)
});

function receiveNewMessage(newMessageContent, userId) {
   if (!newMessageContent){
     return;
   }
   //Get the container for the chat messages. Add a new HTML p element with the inner text of the received message.      
   const chatMessageContainer = document.getElementById("chat-message-container");
   const newMessage = document.createElement("p");
   newMessage.classList.add("message")
   newMessage.innerText = newMessageContent;
   
   //Check if the message was is sent by the user or another user. Add appropriate styling depending on sender.
   if (userId === myUserId) {
       newMessage.classList.add("own-message")
   }
   else {
       newMessage.classList.add("others-message")
   }

   //Add the newly created message to the chat message container and a break line after the message.
   chatMessageContainer.appendChild(newMessage);
   const seperator = document.createElement('br');
   chatMessageContainer.appendChild(seperator);
   }
