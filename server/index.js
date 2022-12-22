const express=require('express');
const socketIO=require('socket.io');
const http=require('http')
const port=5000
var app=express();
let server = http.createServer(app);
var io=socketIO(server);

// app.use(express.static("public"));

// Socket setup
const io = socket(server);

io.on('connection', (socket)=>{
    console.log('New user connected');
     //emit message from server to user
     socket.emit('newMessage', {
       from:'jen@mds',
       text:'hepppp',
       createdAt:123
     });
   
    // listen for message from user
    socket.on('createMessage', (newMessage)=>{
      console.log('newMessage', newMessage);
    });
})