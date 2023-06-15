from bs4 import BeautifulSoup
import requests as req
import re
import os

from requesting_urls import get_html
from collect_dates import find_dates

def extract_events(url):
    '''
    Extract dates, venue and discipline for competitions.

    Args:
        url (str): The url to extract events from
    Returns:
        table_info (list of lists): A nested list where the rows represent each race date, and the columns are [date, venue, discipline].
    '''

    disciplines = {
        "DH": "Downhill",
        "SL": "Slalom",
        "GS": "Giant Slalom",
        "SG": "Super Giant Slalom",
        "AC": "Alpine Combined",
        "PG": "Parallel Giant Slalom "
        }

    # get the html
    html = get_html(url)

    # make soup
    soup = BeautifulSoup(html, "html.parser")

    # Find the tag that contains the Calendar header span
    calendar_header = soup.find(id='Calendar')

    # Find the following table
    calendar_table = calendar_header.find_all_next('table')[0]

    # Find the rows of the first table
    rows = calendar_table.find_all('tr')

    # try parsing the row of ‘th ‘ cells to identify the indices
    th_rows = calendar_table.find_all('th')
    th_dict = {}

    for i, th in enumerate(th_rows):
        th_dict[th.text.strip()] = i

    # for Event , Venue , and Type (discipline)
    found_event = None
    found_date = None
    found_venue = None
    found_discipline = None
    # Saving all necessary values in the list under
    events = []

    full_row_length = len(th_rows)
    short_row_length = full_row_length - 2

    for row in rows:
        cells = row.find_all("td")

        if len(cells) not in range(short_row_length, full_row_length+1):
            # skip rows that don ’t have most columns
            continue

        # Find correct index for event
        event = cells[th_dict['Event']]

        # match event with regex
        if re.match(r"\d{1,3}", event.text.strip()):
            found_event = event.text.strip()
        else:
            found_event = None

        # find the date of the event
        date = cells[th_dict['Date']]
        if len(find_dates(date.text)) == 1:
            found_date = find_dates(date.text)[0]
        else:
            found_date = None

        if len(cells) == full_row_length:
            venue_cell = cells[th_dict['Venue']]
            found_venue = venue_cell.text.strip()
            discipline_index = th_dict['Type']
        else:
            # repeated venue , discipline is in a different column
            diff = full_row_length - len(cells)
            discipline_index = th_dict['Type'] - diff

        discipline = cells[discipline_index]

        discipline_regex = r"((DH)|(SL)|(GS)|(SG)|(AC)|(PG))"
        discipline_match = re.search(discipline_regex, discipline.text.strip())
        if discipline_match:
            # look up the full discipline name
            found_discipline = disciplines[discipline_match.group()]
        else:
            found_discipline = None

        if found_venue and found_event and found_date and found_discipline:
            # if we found something
            events.append((found_date, found_venue, found_discipline))

    return events


def create_betting_slip(events, save_as):
    """
    Saves a markdown format betting slip to the location './datetime_filter/<save_as>.md'.

    Arguments:
        events (list): takes a list of 3-tuples containing date, venue and type for each event.
        save_as (string): filename to save the markdown betting slip as.
    """
    # ensure directory exists
    os.makedirs("datetime_filter", exist_ok=True)

    betting_slip = save_as.replace('_', ' ')

    with open(f"./datetime_filter/{save_as}.md","w") as out_file:
        Date = 'Date'.ljust(12)
        Venue = 'Venue'.ljust(40)
        Discipline = 'Discipline'.ljust(25)

        line_d = ''.ljust(12, '-')
        line_v = ''.ljust(40, '-')
        line_t = ''.ljust(25, '-')

        out_file.write (f"# BETTING SLIP({betting_slip})\n\nName :\n\n")
        out_file.write (f"{Date} | {Venue} | {Discipline} | Who wins?\n")
        out_file.write (f"{line_d} | {line_v} | {line_t} | {line_d} \n")
        for e in events :
            date, venue, type = e
            date = date.ljust(12)
            venue = venue.ljust(40)
            type = type.ljust(25)
            out_file.write(f"{date} | {venue} | {type} | \n")


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup'
    events = extract_events(url)
    create_betting_slip(events, '2021-22_FIS_Alpine_Ski_World_Cup')
