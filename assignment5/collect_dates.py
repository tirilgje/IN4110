import re
from requesting_urls import get_html


def find_dates(html_string, output=None):
    '''
    Finds all dates in a html string.

    The retuned list is in the following format: yyyy/mm/dd

    The following formats are considered when searching:
    DMY : 13 Oct(ober) 2020
    MDY : Oct(ober) 13, 2020
    YMD : 2020 Oct(ober) 13
    ISO : 2020-10-13


    Arguments:
        html_string (str): the html text
        output (str) [optional, default=None]: the name of the output string
    Retunrns:
        dates (list): A list with all the dates found in yyyy/mm/dd format.
    '''

    all_dates = []

    #regex for day
    day = r"\b[0-3]?[0-9]\b"
    day_iso = r"\b[0-3][0-9]\b"

    #regex for year
    year = r"\b[1-2][0-9]{3}\b"

    #regex for months
    jan = r"\b[jJ]an(?:uary)?\b"
    feb = r"\b[fF]eb(?:ruary)?\b"
    mar = r"\b[mM]ar(?:ch)?\b"
    apr = r"\b[aA]pr(?:il)?\b"
    may = r"\b[mM]ay\b"
    jun = r"\b[jJ]un(?:e)?\b"
    jul = r"\b[jJ]il(?:y)?\b"
    aug = r"\b[aA]ug(?:ust)?\b"
    sep = r"\b[sS]ep(?:tember)?\b"
    oct = r"\b[oO]ct(?:ober)?\b"
    nov = r"\b[nN]ov(?:ember)?\b"
    dec = r"\b[dD]ec(?:ember)?\b"

    months = rf"(?:{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{oct}|{nov}|{dec})"

    month_iso = r"\b(?:0[1-9]|1[0-2])\b"


    month_to_dig = {'january':'01', 'jan':'01',
                    'february':'02', 'feb':'02',
                    'march':'03', 'mar':'03',
                    'april':'04', 'apr':'04',
                    'may':'05',
                    'june':'06', 'jun':'06',
                    'july':'07', 'jul':'07',
                    'august':'08', 'aug':'08',
                    'september':'09', 'sep':'09',
                    'october':'10', 'oct':'10',
                    'november':'11', 'nov':'11',
                    'december':'12', 'dec':'12'}

    dmy = rf"{day}\s{months}\s{year}"
    mdy = rf'{months}\s{day},\s{year}'
    ymd = rf'{year}\s{months}\s{day}'
    iso = rf'{year}-{month_iso}-{day_iso}'

    formats = [dmy, mdy, ymd, iso]

    for format in formats:
        date_matches = re.findall(rf"{format}", html_string)

        for match in date_matches:
            if format != iso:
                if format == dmy:
                    match = re.sub(rf"({day})\s({months})\s({year})", r"\3/\2/\1", match)

                elif format == mdy:
                    match = re.sub(rf"({months})\s({day}),\s({year})", r"\3/\1/\2", match)

                elif format == ymd:
                    match = re.sub(rf"({year})\s({months})\s({day})", r"\1/\2/\3", match)

                match = re.sub(rf"({months})", lambda x: month_to_dig[x.group().lower()], match)
                match = re.sub(rf"({day})", lambda x: x.group().zfill(2), match)

            else:
                match = re.sub(rf"({year})-({month_iso})-({day_iso})", r"\1/\2/\3", match)

            all_dates.append(match)

    all_dates.sort()

    if output is not None:
        if not isinstance(output, str):
            raise TypeError('output must be a string')

        #make sure the file is .txt
        if output.find('.') > 0:
            filename, ext = output.split('.')
            if ext != '.txt':
                ext = '.txt'
            output_filename = filename + ext
        else:
            output_filename = output + '.txt'

        #write to file
        with open(output_filename, 'w') as f:
            for date in all_dates:
                f.write(date + '\n')


    return all_dates


if __name__ == '__main__':


    test_urls = ['https://en.wikipedia.org/wiki/J._K._Rowling',
                 'https://en.wikipedia.org/wiki/Richard_Feynman',
                 'https://en.wikipedia.org/wiki/Hans_Rosling']

    outputs = ['J_K_Rowling', 'Richard_Feynman', 'Hans_Rosling']

    base_url = 'https://en.wikipedia.org'
    path = 'collect_dates_regex/'

    for url, out in zip(test_urls, outputs):
        html_string = get_html(url)
        dates = find_dates(html_string, output=path+out)
        print(url, len(dates))
