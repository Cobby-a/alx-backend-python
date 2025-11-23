# from django.urls import path, include
# from rest_framework import routers
# from . import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'conversations', views.ConversationViewSet)
# router.register(r'messages', views.MessageViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# messaging_app/chats/urls.py

from django.urls import path, include
from rest_framework_nested import routers # Import from the installed package
from . import views

# 1. Main (Parent) Router for top-level resources (Conversations, Users)
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'conversations', views.ConversationViewSet)

# 2. Nested Router for nested resources (Messages)
# Messages are nested under a specific conversation
conversations_router = routers.NestedDefaultRouter(
    router, r'conversations', lookup='conversation'
)

# Register the MessageViewSet on the nested router
# This creates routes like /conversations/{conversation_pk}/messages/
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')

# Combine the URL patterns from both routers
urlpatterns = [
    # Include all top-level routes
    path('', include(router.urls)),
    # Include all nested routes (messages)
    path('', include(conversations_router.urls)),
]