import requests
import json
from bs4 import BeautifulSoup

URL = 'https://www.marathonbet.ru/su/live/animation/statistic.htm?treeId='

def getStat(id):
    statLink = URL + id
    response = requests.get(statLink, auth=('user', 'passwd'))

    temp = response.content
    soup = BeautifulSoup(temp, features="html.parser")
    lst = soup.find_all('script')

    statistic = str(lst[2])[str(lst[2]).index('reactData') + 12: str(lst[2]).index(']]>>') - 5]

    statistic_json = json.loads(statistic)
    all_events = statistic_json['liveStatistic']

    homeTeam = {
        'homeTeam': all_events['homeTeam'],
        'Substitution': all_events['statistic']['items']['SUBSTITUTION']['t1'],
        'Foul':all_events['statistic']['items']['FOUL']['t1'],
        'Corner:':all_events['statistic']['items']['CORNER']['t1'],
        'GoalPenalty':all_events['statistic']['items']['GOAL_PENALTY']['t1'],
        'Offside:':all_events['statistic']['items']['OFFSIDE']['t1'],
        'YellowCard':all_events['statistic']['items']['YELLOW_CARD']['t1'],
        'RedCard':all_events['statistic']['items']['RED_CARD']['t1'],
        #'Possession':all_events['statistic']['items']['POSSESSION']['t1'],
        'DangerousAttack':all_events['statistic']['items']['DANGEROUS_ATTACK']['t1'],
        'ShotOnTarget':all_events['statistic']['items']['SHOT_ON_TARGET']['t1'],
        'FreeKick':all_events['statistic']['items']['FREE_KICK']['t1'],
        'Attack':all_events['statistic']['items']['ATTACK']['t1'],
        'Shot':all_events['statistic']['items']['SHOT']['t1']
    }

    awayTeam = {
        'awayTeam': all_events['awayTeam'],
        'Substitution': all_events['statistic']['items']['SUBSTITUTION']['t2'],
        'Foul': all_events['statistic']['items']['FOUL']['t2'],
        'Corner:': all_events['statistic']['items']['CORNER']['t2'],
        'GoalPenalty': all_events['statistic']['items']['GOAL_PENALTY']['t2'],
        'Offside:': all_events['statistic']['items']['OFFSIDE']['t2'],
        'YellowCard': all_events['statistic']['items']['YELLOW_CARD']['t2'],
        'RedCard': all_events['statistic']['items']['RED_CARD']['t2'],
        #'Possession': all_events['statistic']['items']['POSSESSION']['t2'],
        'DangerousAttack': all_events['statistic']['items']['DANGEROUS_ATTACK']['t2'],
        'ShotOnTarget': all_events['statistic']['items']['SHOT_ON_TARGET']['t2'],
        'FreeKick': all_events['statistic']['items']['FREE_KICK']['t2'],
        'Attack': all_events['statistic']['items']['ATTACK']['t2'],
        'Shot': all_events['statistic']['items']['SHOT']['t2']
    }

    ###
    statData = open(id + '.json', 'w')
    statData.write(str(homeTeam) + '\n')
    statData.write(str(awayTeam))
    statData.close()
    ###

    #return [homeTeam,awayTeam]

def getId():

    response = requests.get('https://www.marathonbet.ru/su/live/26418')
    soup = BeautifulSoup(response.content, features="html.parser")

    lst = soup.find_all('script')
    open_bracket_pos = str(lst[2]).index('liveMenuEvents')
    close_bracket_pos = str(lst[2]).rindex('animationWidgetUrl')
    data = "{" + str(lst[2])[ open_bracket_pos - 1 : close_bracket_pos - 2 ] + "}"

    json_data = json.loads(data)
    all_events = json_data['liveMenuEvents']
    sport = all_events['childs'][0]['label']
    football_events = all_events['childs'][0]
    events_count = str(football_events).count(''"event"'')

    event_pos = 0
    fstr = str(football_events)

    for i in range (events_count):
        event_pos = fstr.index('event', event_pos + 1)
        uid_pos = fstr.index('uid', event_pos - 30) + 7
        uid_end_pos = fstr.index(',', uid_pos) - 1
        uid = fstr[uid_pos:uid_end_pos]
        getStat(str(uid))


if __name__ == "__main__":
    getId()