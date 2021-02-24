# SοrakaMafaka
# API-Key: API

from riotwatcher import LolWatcher, ApiError
import pandas as pd
import cv2

# Global vars
api_key = 'API KEY'
watcher = LolWatcher(api_key)
my_region = 'eun1'
region = 'eune'

# Check league's latest version
latest = watcher.data_dragon.versions_for_region(region)['n']['champion']
# Champions static information
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')


# General stats
me = watcher.summoner.by_name(my_region, 'SοrakaMafaka')
# print(me)

# Rank stats
#my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
# print(my_ranked_stats)

my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])

# Fetch details of last match
last_match = my_matches['matches'][0]
match_detail = watcher.match.by_id(my_region, last_match['gameId'])
participants = []
for row in match_detail['participants']:
    participants_row = {}
    participants_row['champion'] = row['championId']
    #participants_row['spell1'] = row['spell1Id']
    #participants_row['spell2'] = row['spell2Id']
    participants_row['win'] = row['stats']['win']
    participants_row['kills'] = row['stats']['kills']
    participants_row['deaths'] = row['stats']['deaths']
    participants_row['assists'] = row['stats']['assists']
    

    #participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
    #participants_row['goldEarned'] = row['stats']['goldEarned']
    #participants_row['champLevel'] = row['stats']['champLevel']
    #participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
    #participants_row['item0'] = row['stats']['item0']
    #participants_row['item1'] = row['stats']['item1']
    participants.append(participants_row)

participantIdentities = []
for row in match_detail['participantIdentities']:
	participantIdentities_row = {}
	participantIdentities_row['summonerName'] = row['player']['summonerName']
	participantIdentities.append(participantIdentities_row)

# Champion static list data to dictionary for looking up
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

for row in participants:
    row['championName'] = champ_dict[str(row['champion'])]


# print(match_detail.keys())

df = pd.DataFrame(participants)
df1 = pd.DataFrame(participantIdentities)
frames = [df, df1]
result = pd.concat(frames, axis=1, join="inner")
print(result.to_string())
# End of fetch deails of last match
