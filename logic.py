from funtions import *

# init html content
content = get_website_content("https://www.hltv.org/results","div", "result-con", "multi")

map_base_stats = get_match_overview(content)
matches_links = get_matches_links(content)
players_stats = get_players_played(matches_links[4])

# both works fine
write_to_file(map_base_stats, "map_base_stats.txt", "listdict")
write_to_file(players_stats, "players_stats.txt", "listdict")
