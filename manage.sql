select first_name ||' '|| last_name as full_name, title, maker, number_of_players, skill_level, game_type_id 
from auth_user join levelupapi_game on gamer_id=auth_user.id