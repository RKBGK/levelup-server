"""View module for handling requests about game types"""
from multiprocessing import Event
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models.game import Game
from levelupapi.models.game_type import GameType
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError
# from rest_framework.decorators import  permission_classes
# from rest_framework.permissions import AllowAny

class GameView(ViewSet):
    """Level up game types view"""
    
    # @permission_classes([AllowAny])
    def retrieve(self, request, pk):
        games = Game.objects.get(pk=pk)
        serializer = GameSerializer(games)
        return Response(serializer.data)
        
    # @permission_classes([AllowAny])
    def list(self, request):
        games = Game.objects.all()
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
            
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    # def create(self, request):

    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     game_type = GameType.objects.get(pk=request.data["game_type"])

    #     game = Game.objects.create(
    #         title=request.data["title"],
    #         maker=request.data["maker"],
    #         number_of_players=request.data["number_of_players"],
    #         skill_level=request.data["skill_level"],
    #         gamer=gamer,
    #         game_type=game_type
    #     )
    #     serializer = GameSerializer(game)
    #     return Response(serializer.data)
    # this will replace the previous create method
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        gamer = Gamer.objects.get(user=request.auth.user)
        # game_type = GameType.objects.get(pk=request.data["game_type"])
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        game = Game.objects.get(pk=pk) 
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        game.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
                

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'title','maker','number_of_players','skill_level','game_type','gamer')
        depth = 2
        
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']        