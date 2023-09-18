from bs4 import BeautifulSoup
import json
import re

URL = "https://www.thebaseballcube.com/content/current_rosters/23/"
headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

FIELD_MAPPINGS = {
        "player name": "player_name",
        "pos": "position",
        "age": "age",
        "statusshort": "current_status",
        "ht": "height",
        "wt": "weight",
        "ba": "batting_hand",
        "th": "throwing_hand",
        "Born": "birthday",
        "place": "hometown",
        "hilvl": "highest_level_played",
        "mlb years": "year_in_mlb",
        "stat years": "stat_years",
        "draft info": "draft_info"
    }


def load_table_from_file():
    table_text = ''
    with open("page_content.html", "r") as file:
        table_text = ''.join(file.readlines())

    return table_text


def convert_table_to_json(html_table):
    # Parse the HTML content
    soup = BeautifulSoup(html_table, 'html.parser')

    # Find the table element
    table = soup.find('table', class_='rankings__table--team')
    rows = table.tbody.find_all('tr', class_='sc-VigVT efItBJ')

    data = []

    for row in rows:
        cells = row.find_all('td')
        rank = cells[0].text
        player = cells[1].find_all(class_='prospect-headshot__name')[0].text
        position = cells[2].text
        team_logo = cells[3].div.img['src']
        team_name = cells[3].div.div.text
        level = cells[4].text.strip()
        eta = cells[5].text
        age = cells[6].text
        height_weight = cells[7].text
        bats = cells[8].text
        throws = cells[9].text

        # https://www.mlb.com/prospects/pirates/paul-skenes-694973
        photo_url = cells[1].img['src']
        re_result = re.search(r'/(\d+)/headshot/', photo_url)
        if re_result is not None:
            player_id = re_result.group(1)
        else:
            print(f"Bad photo url found: {photo_url} for player: {player}")
            player_id = 0
        player_slug = player.lower().replace(" ", "-")
        link = f"https://www.mlb.com/prospects/pirates/{player_slug}-{player_id}"

        player_data = {
            'Rank': rank,
            'Player': player,
            'Player_Link': link,
            'Position': position,
            'Team_Logo': team_logo,
            'Team_Name': team_name,
            'Level': level,
            'ETA': eta,
            'Age': age,
            'Height_Weight': height_weight,
            'Bats': bats,
            'Throws': throws
        }

        data.append(player_data)

    # Save the JSON data
    with open("prospects.json", "w+") as file:
        file.write(json.dumps(data))


if __name__ == '__main__':
    html_table = load_table_from_file()
    convert_table_to_json(html_table)
