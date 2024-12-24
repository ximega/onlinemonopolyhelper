
# Requirements:
- Python of version 3.13.0
- Django 5.1.3 (Install by running `pip install django==5.1.3`)

# Install

#### Through git (must have git pre-installed)
1. Open directory where you want to place the game
2. Paste and run
```
git clone https://github.com/ximega/onlinemonopolyhelper.git
```

#### Direct download
1. Go to releases and select the version https://github.com/ximega/onlinemonopolyhelper/releases
2. Install the release
3. Place the files in a directory

# How to play
0) If want to reset all data run:
```
python3 manage.py resetgame
```
1) Run by
```
python3 manage.py runserver 0.0.0.0:8000
```
2) Find your ip address on your system
3) Paste to a browser: [your_ip]:8000

`NOTE`: only players connected to the same network will be able to connect to server and play

### Creating a host (preferably only 1 person should be hosting)
1. Run
```
python3 manage.py createsuperuser
```
2. Fill inputs

### Creating new players:
1. Run
```
python3 manage.py createdefaultuser
```
2. Fill inputs

## Text

`NOTE`: most of the text is written in Russian, thought you can edit it

1. Open all info.py files in following directories:
```
login/
cadmin/
dashboard/
onlinemonopolyhelper/
stats/
```
2. Write text in your own language

## Monopoly types
You can add your own monopoly type with names, how much regions cost and hotel prices. (Unfortunately games with homes is now not supported)

The following structure must be followed for all new types
```
[type_name]/
    regions/
        buy.json
        hotels.json
        list.json
    data.json
```

Inside `[type_name]/data.json` following info must be put:
```
{
    "name": "[type_name]",
    "regions_count": [int],
    "initial_balance": [int],
    "max_hotels_on_region": [int]
}
```

`list.json` must contain a list of all regions
`buy.json` must contain a dictionary of [RegionName, BuyingPrice]
`hotels.json` must contain a dictionary of [RegionName, BuildingPrice]


Place new type inside `games/`
But you can edit this folder inside `dashboard/models.py`, editing `GAMES_PATH`

Make sure to also edit `games/data.json` and put your new type there inside `"game_types"`
Only path variable should be specified inside

## Logs

The logs are created each time `runserver` is run. You can check those inside `logs/` directory. 

If log was created 20 minutes ago it will be deleted forever during the next run of `runserver`


# User Interface
\* - an interface part might not appear straightaway, only when there is a need for that

\*\* - if there are available regions

## Info
- Current balance
- Regions an user owns *
- Top players
- Last receiver, last sent, and last paid (for bills, which are fines most of the time)
## Requests
- Bills *
- Incoming region transfer requests *
## Forms
- Transfer money
- Request to buy a region (from bank/host) **
- Request to build a hotel (from bank/host) *
- Request to sell an owned region (to bank/host) * 
- Request to exchange a property for money with another player *

# Host interface (CAdmin)

## Requests
- Requests to buy a region *
- Requests to build a hotel on a region *
- Requests to exchange a region between players (a host simply should confirm this transfer) *
## Forms
- To give 200$ when player passes an initial field
- Give money from bank (any amount)
- Send bill (mostly for fines)
- Set balance of a player manually