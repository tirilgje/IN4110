
from requesting_urls import get_html
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#5.5.1 Get the list of teams
def extract_urls(table, base_url):
    '''
    Extract the team urls for the temas in the semifinals in the bracket table

    Arguemtns:
        table (bs4 element): The table cotaining the team urls
        base_url (str): base_url for the wikipedia page
    Returns:
        urls (list): List of the urls
    '''
    urls = []

    #find urls in the table
    for url in table.find_all('a'):
        if url is not None:
            url = url.get('href')
            urls.append(base_url + url)

    # filter out urls for teams in semifinals
    # these urls is to be found more than once
    urls = list(set(filter(lambda x: urls.count(x) > 1, urls)))
    urls.sort()

    return urls

#5.5.1 Get the list of teams
def extract_teams(url, base_url=None):
    """
    Extract team names and urls from the NBA Playoff ’Bracket’ section table .

    Arguments:
        url (str): the url to chech out
        base_url (str) [optional, default=None]: Base url for the url

    Returns :
        team_names (list): A list of team names that made it to the conference semifinals .
        team_urls (list): A list of absolute Wikipedia urls corresponding to team_names.
    """
    # get html using for example get_html from requesting_urls
    html = get_html(url)

    # create soup
    soup = BeautifulSoup(html, "html.parser")
    # find bracket we are interested in
    bracket_header = soup.find(id="Bracket")
    bracket_table = bracket_header.find_next("table")
    rows = bracket_table.find_all("tr")

    # create lists of team names
    team_names = []

    for i in range(1, len(rows)):
        cells = rows[i].find_all("td")
        #print(cells)
        cells_text = [cell.get_text(strip=True) for cell in cells]

        # Filter out the cells that are empty
        cells_text = [cell for cell in cells_text if cell]

        # Find the rows that contain seeding, team name and games won
        if len (cells_text) > 1:
            team_name = cells_text[1].strip('*')
            team_names.append(team_name)

    # Filter out the teams that appear more than once
    team_names = list(set(filter(lambda x: team_names.count(x) > 1, team_names)))
    team_names.sort()

    # Get team urls for the teams in the semifinals
    team_urls = extract_urls(bracket_table, base_url)

    return team_names, team_urls

#5.5.2 - Get the list of players
def extract_players(team_url, base_url=None):
    """
    Extract players that played for a specific team in the NBA playoffs.

    Arguments:
        team_url (str): URL to the Wikipedia article of the season of a given team.
        base_url (str) [optional, default=None]: Base url for the url

    Returns:
        player_names (list): A list of players names corresponding to the team whos URL was passed.
        player_urls (list): A list of Wikipedia URLs corresponding to player_names of the team whos URL was passed.

    """
    # keep base url
    if base_url is None:
        base_url = "https://en.wikipedia.org"

    # get html for each page using the team url you extracted before
    html = get_html(team_url)

    # make soup
    soup = BeautifulSoup(html, "html.parser")
    # get the header of the Roster
    roster_header = soup.find(id="Roster")
    # identify table
    roster_table = roster_header.find_next("table")
    rows = roster_table.find_all("tr")

    # creating a dictionary for headers and indexes
    th = roster_table.find_all('th')[2:]
    th_dict = {}

    for i, th in enumerate(th):
        th_dict[th.text.strip()] = i

    # prepare lists for player names and urls
    player_names = []
    player_urls = []

    for i in range (0 , len(rows)):
        cells = rows[i].find_all("td")
        cells_text = [cell.get_text(strip = True) for cell in cells]

        if len (cells_text) == len(th_dict):
            # find player name and urls
            player_name = cells_text[th_dict['Name']]
            rel_url = cells[th_dict['Name']].find_next("a").attrs["href"]

            # add player and url to list
            player_names.append(player_name)
            player_urls.append(base_url + rel_url)

    return player_names, player_urls

#5.5.3 - Get player statistics
def extract_player_statistics(player_url):
    """
    Extract player statistics for NBA player.

    Arguments:
        player_url (str): URL to the Wikipedia article of a player.

    Returns :
        ppg (float): Points per Game .
        bpg (float): Blocks per Game .
        rpg (float): Rebounds per Game .

    """
    # default score as some players have incomplete statistics/information
    ppg = 0.0
    bpg = 0.0
    rpg = 0.0

    # get html
    html = get_html(player_url)

    # make soup
    soup = BeautifulSoup(html, "html.parser")

    # find header of NBA career statistics
    nba_header = soup.find(id="NBA_career_statistics")

    # check for alternative name of header
    if nba_header is None:
        nba_header = soup.find(id="NBA")

    try:
        # find regular season header
        regular_season_header = nba_header.find_next(id="Regular_season")

        # next we should identify the table
        nba_table = regular_season_header.find_next("table")

    except:
        try:
            # table might be right after NBA career statistics header
            nba_table = nba_header.find_next("table")

        except:
            return ppg, bpg, rpg

    # find nba table header and extract rows
    table_header = nba_table.find_all("th")

    columns = {}
    for i, th in enumerate(table_header):
        columns[th.text.strip()] = i

    rows = nba_table.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        cells_text = [cell.get_text(strip = True) for cell in cells]

        if len(cells_text) > 0 and cells_text[0].startswith('2020'):
            ppg = cells_text[columns['PPG']]
            bpg = cells_text[columns['BPG']]
            rpg = cells_text[columns['RPG']]


    # Convert the scores extracted to floats
    try:
        ppg = float(ppg)
    except ValueError:
        ppg = 0.0

    try:
        bpg = float(bpg)
    except ValueError:
        bpg = 0.0

    try:
        rpg = float(rpg)
    except ValueError:
        rpg = 0.0

    return ppg, bpg, rpg

def plot_NBA_player_statistics(teams, color_table, xpg, filename):
    """
    Plot NBA player statistics.

    Arguments:
        teams (list): list of team names
        color_table (dict): dictionary containing one color for each team in teams.
        xpg (str): witch statistics to plot, ppg, bpg or rpg
        filename (str): name of the output file.
    """
    plt.figure()
    count_so_far = 0
    all_names = []

    # iterate through each team and the
    for team, players in teams.items():
        # pick the color for the team , from the table above
        color = color_table[team]
        # collect the ppg and name of each player on the team
        # you ’ll want to repeat with other stats as well
        ppg = []
        names = []
        for player in players:
            names.append(player['name'])
            ppg.append(player[xpg])
        # record all the names , for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players so far
        x = range(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # make bars for this team ’s players ppg ,
        # with the team name as the label
        bars = plt.bar(x, ppg, color=color, label=team )
        # add the value as text on the bars
        plt.bar_label(bars)

    # use the names , rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    # add the legend with the colors for each team
    plt.legend(loc=0)
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title(xpg.upper())
    # save the figure to a file

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.savefig(filename)

def collect_statistics(team_names, team_urls, base_url):
    '''
    Collect the statistics nessesery for the plotting

    Arguments:
        team_names (list): list of the team names
        team_urls (list): list of url for each team in team_names
        base_url (str): the base url for the urls in team_urls

    Returns:
        all_teams (dict): dictionary containing information on the top players in each team
        color_table (dict): dict mapping each team to a color
    '''

    def sort_ppg(p):
        '''Function used for sorting the list team after ppg score'''
        return p['ppg']

    # defines the colors
    colors = ['red', 'orange', 'yellow', 'palegreen', 'cyan', 'blue', 'plum', 'pink']
    color_table = {}

    #mapping team to color
    for i, team in enumerate(team_names):
        color_table[team] = colors[i]

    #dictionary coitaining all teams and the top 3 players with their scores
    all_teams = {}

    for i in range(len(team_names)):
        team_players, player_urls = extract_players(team_urls[i], base_url)

        team = []

        for j in range(len(team_players)):

            ppg, bpg, rpg = extract_player_statistics(player_urls[j])

            #adding statistics for each player to the team
            player = {}
            player['name'] = team_players[j]
            player['ppg'] = ppg
            player['bpg'] = bpg
            player['rpg'] = rpg

            team.append(player)

        # sort players by ppg score, and slice top 3
        team.sort(reverse=True, key=sort_ppg)
        # add a top 3 players of the team to all_teams
        all_teams[team_names[i]] = team[:3]

    return all_teams, color_table


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/2021_NBA_playoffs'
    base_url = 'https://en.wikipedia.org'
    team_names, team_urls = extract_teams(url, base_url=base_url)

    teams, color_table = collect_statistics(team_names, team_urls, base_url)

    for xpg in ['ppg', 'bpg', 'rpg']:
        filename = 'NBA_player_statistics/player_over_' + xpg + '.png'
        plot_NBA_player_statistics(teams, color_table, xpg, filename)
