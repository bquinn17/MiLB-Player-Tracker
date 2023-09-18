import datetime
import math

import requests
from lxml import html
from bs4 import BeautifulSoup
import json

url = "https://www.thebaseballcube.com/content/current_rosters/23/"
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


def download_table():
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to download page. Status code: {response.status_code}")
        return

    print("Page content downloaded successfully.")

    # Parse the HTML content
    parsed_html = html.fromstring(response.content)

    # Extract content using XPath
    extracted_data = parsed_html.xpath('//*[@id="dg_0"]')

    table_text = ''

    if not extracted_data:
        print("XPath did not match any elements on the page.")
        return

    # Print or process the extracted content as needed
    print("Extracted content:")
    for item in extracted_data:
        table_text = html.tostring(item).decode()
        print(table_text)

    with open("page_content.html", "w+") as file:
        file.write(table_text)

    return table_text


def load_table_from_file():
    table_text = ''
    with open("page_content.html", "r") as file:
        table_text = ''.join(file.readlines())

    return table_text


def convert_table_to_json(html_table):
    # Parse the HTML content
    soup = BeautifulSoup(html_table, 'html.parser')

    # Find the table element
    table = soup.find('table', {'id': 'dg_0'})

    # Initialize an empty list to store rows
    data = []

    # Find all rows in the table
    rows = table.find_all('tr', class_='dataRow')
    table_header = table.find_all('tr', class_='headerRow')[0].find_all('td')

    for i in range(len(table_header)):
        header_value = table_header[i].text.strip()
        if header_value in FIELD_MAPPINGS:
            header_value = FIELD_MAPPINGS[header_value]
        else:
            print("Header value not found: ", header_value)
        table_header[i] = header_value

    # Iterate through each row
    for row in rows:
        # Initialize an empty dictionary to store row data
        row_data = {}

        # Find all cells in the row
        cells = row.find_all('td')

        # Iterate through each cell
        for i, cell in enumerate(cells):
            # Get the column header
            header = table_header[i]

            # Check if the cell contains a link
            link = cell.find('a')
            if link:
                # If a link is found, add it to the row data
                link_url = link['href']
                row_data[f'{header}_link'] = link_url

            # Get the cell value
            value = cell.text.strip()

            if header == 'age':
                value = str(math.floor(float(value)))

            # Add the data to the row dictionary
            if header != '':
                row_data[header] = value

        # Append the row dictionary to the data list
        data.append(row_data)

    # Convert the data list to JSON
    json_data = json.dumps(data, indent=4)

    check_for_updates(data)

    print("Total number of players found: ", len(data))

    # Save the JSON data
    with open("top_players.json", "w+") as file:
        file.write(json_data)


def check_for_updates(new_player_json):
    old_player_json = ''
    with open("top_players.json", "r") as file:
        old_player_json = json.load(file)

    updates_list = []

    for i in range(len(new_player_json)):
        old_player_obj = old_player_json[i]
        new_player_obj = new_player_json[i]

        for key in new_player_obj:
            if new_player_obj[key] != old_player_obj[key]:
                print("Update found to player data: ")
                status_update = f"changed {key} from {old_player_obj[key]} to {new_player_obj[key]}"
                date = str(datetime.date.today())
                update_message = f"Player: {new_player_obj['player_name']} {status_update} on date: {date}"
                print(update_message)

                update_json = {
                    "player_name": new_player_obj['player_name'],
                    "status_update": status_update,
                    "date": date,
                    "player_url": new_player_obj['player_name_link']
                 }
                updates_list.append(update_json)

    old_updates = []
    with open("roster_updates.json", "r") as file:
        old_updates = json.load(file)

    with open("roster_updates.json", "w+") as file:
        if isinstance(old_updates, list):
            old_updates.extend(updates_list)
        file.write(json.dumps(old_updates))


if __name__ == '__main__':
    html_table = download_table()
    # html_table = load_table_from_file()
    convert_table_to_json(html_table)
