# from django.urls import path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import accounts.routing
#
# # websocket_urlpatterns = [
# #     url(r'^ws/accounts/(?P<room_name>[^/]+)/', ConsumerConnection),
# # ]
#
# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': AuthMiddlewareStack(
#         URLRouter([
#             accounts.routing.websocket_urlpatterns
#         ])
#     ),
# })
