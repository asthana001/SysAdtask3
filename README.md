# DeltaSysadTask3
A chat room using python socket programming for soldiers

# User Manual
* Ensure python of version more than ```3.6``` is installed in your computer.
* Open the terminal inside your cloned folder and run python ```server.py```
* Now,the server will be listening on connections in ```IP 127.0.0.1``` and ```port 6060```
* Then, run python ```client.py``` to create a memeber of the chat room.
* Any message sent by the client is sent to all other members of the room
* To get chat history send the message ```chat-history``` through any client and a file with the name of the client containing chat history is created
* To quit the chat send the message ```quit``` through any client and you will he removed from the chat
