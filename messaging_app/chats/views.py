from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


# ---------------------------------------------------
# Conversation ViewSet
# ---------------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Expected payload:
        { "participants": [user_id1, user_id2] }
        """
        participants = request.data.get("participants")

        if not participants or len(participants) < 2:
            raise ValidationError("A conversation must include at least two participants.")

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------
# Message ViewSet
# ---------------------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expected payload:
        {
            "conversation": "<conversation_id>",
            "sender": "<user_id>",
            "message_body": "Hello!"
        }
        """
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")
        sender = request.data.get("sender")

        if not conversation_id or not sender:
            raise ValidationError("conversation and sender fields are required.")

        if not message_body:
            raise ValidationError("Message body cannot be empty.")

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist.")

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
