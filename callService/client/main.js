var socket = io();

var form = document.querySelector('form');


form.addEventListener('submit', function(e) {
  e.preventDefault();
  var input = document.querySelector('#message');
  var text = input.value;
  socket.emit('message', text);
  input.value = '';
});

socket.on('message', text => {
  receiveNewMessage(text)
  });


socket.on("user-connected",  () => {
  console.log("user connected");
  newUserConnected();

})

function newUserConnected() {
  const userContainer = document.getElementById("active-user-container");
  const newUser = document.createElement("p")
  newUser.innerText = "Ny bruker logget på"
  userContainer.appendChild(newUser);
}

function receiveNewMessage(newMessageContent) {
  if (!newMessageContent){
    return;
  }
  console.log(newMessageContent)

  var videoGrid = document.getElementById("video-grid");
  var newMessage = document.createElement("div");
  newMessage.innerText = newMessageContent;
  videoGrid.appendChild(newMessage);

  var seperator = document.createElement('br');
  videoGrid.appendChild(seperator);

  videoGrid.scrollTop = videoGrid.scrollHeight;
}


const videoGrid = document.getElementById('video-grid')
const myVideo = document.createElement('video')
myVideo.muted = true

navigator.mediaDevices.getUserMedia({
  video: true,
  audio: true
}).then(stream => {
  addVideoStream(myVideo, stream)
})

function addVideoStream(video, stream) {
  console.log("add video stream called")
  video.srcObject = stream
  video.addEventListener('loadedmetadata', () => {
    video.play()
  })
  videoGrid.append(video)
}
