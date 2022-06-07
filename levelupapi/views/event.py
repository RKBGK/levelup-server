"""View module for handling requests about game types"""
from multiprocessing import Event
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models.game_type import GameType
from levelupapi.models.game import Game
from levelupapi.models.gamer import Gamer
# from rest_framework.decorators import  permission_classes
# from rest_framework.permissions import AllowAny

class EventView(ViewSet):
    """Level up game types view"""
    
    # @permission_classes([AllowAny])
    def retrieve(self, request, pk):
        try:
            events = Event.objects.get(pk=pk)
            serializer = EventSerializer(events)
            return Response(serializer.data)
        except Event as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    # @permission_classes([AllowAny])
    def list(self, request):
        events = Event.objects.all()
        event_game = request.query_params.get('game', None)
        if event_game is not None:
            events = events.filter(game_id=event_game)
            
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


    
    # def create(self, request):

    #     game = Game.objects.get(pk=request.data["game"])
    #     organizer = Gamer.objects.get(user=request.auth.user)

    #     event = Event.objects.create(
    #         game=game,
    #         description=request.data["description"],
    #         date=request.data["date"],
    #         time=request.data["time"],
    #         organizer=organizer
    #     )
    #     serializer = EventSerializer(event)
    #     return Response(serializer.data)
    def create(self, request):

        # game = Game.objects.get(pk=request.data["game"])
        organizer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  
    
    
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'description','date','time','game','organizer')
        depth = 2
        
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'description','date','time','game']  