"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection 
from django.views import View
from levelupapi.models import  Game
from levelupreports.views.helpers import dict_fetch_all


class UserGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            select first_name ||' '|| last_name as full_name, title, maker, number_of_players, skill_level, game_type_id , gamer_id
            from auth_user join levelupapi_game on gamer_id=auth_user.id
            """)
        
            games_by_user = [] 
            
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            games_by_user = [] 
            for row in dataset:

                game = Game(row['game_type_id'] ,row['title'], row['maker'],row['gamer_id'], 
                            row['number_of_players'],row['skill_level'] )

                
                user_dict = next(
                    (
                        user_game for user_game in games_by_user
                        if user_game['gamer_id'] == row['gamer_id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    user_dict['games'].append(game)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    games_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "games": [game]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "usergame_list": games_by_user
        }

        return render(request, template, context)
