from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
# CON_LIST = []

class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print(message,"connected...",)
        self.accept()
        self.send("this is not true\n")
        # CON_LIST.append(self)

    def websocket_receive(self, message):
        print(message,"<-message received")
        self.send("this is not true\n")
        async_to_sync(self.channel_layer.group_add)("group0",self.channel_name)
    
    def websocket_disconnect(self, message):
        print(self.channel_name," disconnected ")
        raise StopConsumer()
        

    

