# # from channels import Group
# import json
# from channels.generic.websocket import AsyncConsumer
# from asgiref.sync import async_to_sync
#
# class MyConsumer(AsyncConsumer):
#
#     async def websocket_connect(self, event):
#         # Called when a new websocket connection is established
#         print("connected", event)
#         user = self.scope['user']
#         self.update_user_status(user, 'online')
#
#     async def websocket_receive(self, event):
#         # Called when a message is received from the websocket
#         # Method NOT used
#         print("received", event)
#
#     async def websocket_disconnect(self, event):
#         # Called when a websocket is disconnected
#         print("disconnected", event)
#         user = self.scope['user']
#         self.update_user_status(user, 'offline')
#     # def ws_connect(self):
#     #     # Group('users').add(message.reply_channel)
#     #     async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
#     #
#     #
#     # def ws_disconnect(self, close_code):
#     #     Group('users').discard(message.reply_channel)
#     #
#     # def receive(self, text_data):
#     #     async_to_sync(self.channel_layer.group_send)(
#     #         "chat",
#     #         {
#     #             "type": "chat.message",
#     #             "text": text_data,
#     #         },
#     #     )
#     #
#     # def chat_message(self, event):
#     #     self.send(text_data=event["text"])
