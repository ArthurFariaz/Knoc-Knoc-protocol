# Knoc-Knoc-protocol
    This project implements the Knock Knock protocol in Python. The Knock Knock protocol is a simple TCP protocol used to test if a server is online. The client sends a "knock knock" message to the server. If the server is online, it will respond with a knock knock joke. The server and the client will exchange messages until the joke is finished.
## references: 
* [socket docs](https://docs.python.org/3/library/socket.html)
* [forum about python](https://realpython.com/python-sockets/)
### TODO:
- [x] Bug fix client -- the client can blow up the server with some inputs.
- [x] Knoc knoc protocol -- the mensagens the server receive, must gain a function.
- [ ] Create a queue for the clients.