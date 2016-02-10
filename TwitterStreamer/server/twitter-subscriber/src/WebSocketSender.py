from websocket_server import WebsocketServer
from threading import Thread

"""A super-simple class that simply creates a WebSocket connection and sends messages to it. Ideally, this class should:
- have failover logic
- have dynamic port creation
- something slightly more elegant than sending the message to _all_ clients.
However, for the purposes of this task, it might just about do the job.
"""


class WebSocketSender:
  def send(self, data):
    """Sends message (i.e. the coordinates) to all clients connected to this WebSocket server.
      :param data: the message that needs to be sent over the websocket. In this case, it's the lat-long of the
    tweet.
    """
    self.server.send_message_to_all(data)

  def acknowledgeNewClient(self, client, server):
    """
    When a new client connects to the WebSocket, this simply acknowledges
    :param client: The details of the client that connects to the websocket, including the IP and port.
    :param server: The websocket server that includes details of where the websocket server is running (including
          the IP and port, and the existing list of clients.
    """
    print("New client connected: {}".format(client))

  def startWebSocketServer(self):
    """Initialises the WebSocketServer on port 8080. What should happen if the port is already occupied?
    Should we try to set the port dynamically? Or, simply fail fast?"""
    try:
      self.server.set_fn_new_client(self.acknowledgeNewClient)
      self.server.run_forever()
    except Exception as ex:
      print("Caught exception while attempting to start the WebSocketServer")
      print(ex)

  def __init__(self):
    self.server = WebsocketServer(8080)
    t = Thread(target=self.startWebSocketServer)
    t.start()
