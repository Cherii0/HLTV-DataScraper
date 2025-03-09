from funtions import *

history_results_pages = 2
links = get_matches_links(history_results_pages)

for link in links:
    match = get_match(link)
    write_to_file(match, "matches.txt", "listdict")
