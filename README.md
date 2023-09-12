# MiLB-Player-Tracker

## Sites of Interest

- MiLB.com player lookup
  - https://www.milb.com/player/coby-mayo-691723
- MLB Top 100 Prospects
  - https://www.mlb.com/prospects/stats/top-prospects
- Pirates Top (30) Prospects
  - https://www.mlb.com/prospects/pirates/
- Pirates 40 man roster
  - https://www.thebaseballcube.com/content/current_rosters/23/
- MLB Search by hometown
  - https://www.thebaseballcube.com/content/city/1678/#
- MiLB Advanced stats
  - https://milbtracker.com/hitter-stats
  - https://www.fangraphs.com/players/ryan-ward/sa1169792/stats?position=OF
- Baseball Reference
  - More Player info https://www.baseball-reference.com/players/a/altuvjo01.shtml
  - Team Info: https://www.baseball-reference.com/teams/PIT/2023.shtml

## Django Tips

Activate venv on Windows:

- `venv\Scripts\activate.ps1` (from django-backend folder)

Useful Django commands:

- `python authored\manage.py makemigrations` and `python authored\manage.py migrate` Run anytime the models are changed for an app

- `python authored\manage.py runserver` Start the server (from django-backend/authored folder)

- `python authored\manage.py createsuperuser --email admin@example.com --first_name Bryan --last_name Quinn --role Author` Add user account after DB deleted

- `cd authored && pytest` Run the unit tests (must be done from the authored folder)

## Dashboard Templates

- https://medium.com/@appseed.us/django-dashboards-open-source-and-free-projects-1d8e64919e6d
