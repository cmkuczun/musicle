from queries import *
from datetime import *

# sample use for some functions
# candidates = get_id_from_song('horse')

# for song_id in candidates:
#     print(song_id)
#     output = get_song_stats(song_id)
#     pprint.pprint(output)
 
res = load_user_recent_games(60)
print(res)