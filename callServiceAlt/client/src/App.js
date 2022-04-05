import './App.css';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';

//const socket = io.connect("http://localhost:3001")
const socket = io("https://call-service-server.herokuapp.com/", {transports: ["polling", "websocket"]});


export default function App() {

  const [message, setMessage] = useState("")
  const [receivedMessages, setReceivedMessages] = useState([])

  function sendMessage() {
    socket.emit("sendMessage", {message})
  }

  useEffect(() => {
    socket.on("receivedMessage", (message) => {
      console.log(message)
      setReceivedMessages([...receivedMessages, message.message])
    })
  }, [socket])

  return (
    <div className="App">
      <input placeholder="Message" onChange={(e) => setMessage(e.target.value)}/>
      <button onClick={sendMessage}>Send message</button>
      {receivedMessages.map( message => {
        return <p>{message.message}</p>
      })}
    </div>
  );
}