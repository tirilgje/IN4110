from bs4 import BeautifulSoup
from requesting_urls import get_html
from filter_urls import find_urls, find_articles
import time

import random
from collections import deque


def shortest_path(start_url, final_url, base_url='https://en.wikipedia.org'):
    '''
    Find the shortest path between two urls using the bfs

    Arguments:
        start_url (str): The url to start from
        final_url (str): The url to find the path to

        base_url (str) [optional, default='https://en.wikipedia.org']: The base_url for article searching.

    Returns:
        full_path (list): List of articles in the path from start_url to final_url.

        (None if no path are found)
    '''
    # dictionary to keep track of path from all urls visited back to start_url
    path = {}
    path[start_url] = [start_url]
    #queue for the articles to check out
    #using degue to make it faster to pop and append elements
    que = deque([start_url])

    while len(que) > 0:
        # find next article from the que to visit
        next = que.popleft()
        #print(next)
        # Find all the articles in this article
        next_html = get_html(next)
        articles = find_articles(next_html, base_url, en_only=True)

        for article in articles:
            if article == final_url:
                # found the correct url
                print("win", article)
                full_path = path[next] + [article]
                return full_path

            if article not in path:
                #save the path to this article and add it to the que
                path[article] = path[next] + [article]
                que.append(article)

    #return none if all articles are checked at no path are found.
    return None


def write_to_file(output_filename, path, time):

    '''
    Writes runtime and path between two articles to file

    Arguments:
        output_filename (str): name of the output file
        path (list): list cotaining the path
        time (float): the time it took to find the path
    '''

    with open(output_filename, 'w') as f:
        f.write('Start url: ' + path[0] + '\n')
        f.write('Final url: ' + path[-1] + '\n')
        f.write('Number of articles visited: ' + str(len(path)) + '\n')
        f.write('Time used: ' + str(round(time, 3)) + ' sec \n')
        f.write('The full path: \n')
        for article in path:
            f.write('   ' + article + '\n')


if __name__ == '__main__':

    base_url = 'https://en.wikipedia.org'

    start_url1 = 'https://en.wikipedia.org/wiki/Parque_18_de_marzo_de_1938'
    final_url1 =  'https://en.wikipedia.org/wiki/Bill_Mundell'


    start_url2 = 'https://en.wikipedia.org/wiki/Nobel_Prize'
    final_url2 = 'https://en.wikipedia.org/wiki/Array_data_structure'
    out2 = 'wiki_race_challange/shortest_path.txt'

    start_url3 = 'https://en.wikipedia.org/wiki/Nobel_Prize'
    final_url3 = 'https://en.wikipedia.org/wiki/Natural_science'
    out3 = 'wiki_race_challange/shortest_path_test.txt'


    #t0 = time.time()
    #path3 = shortest_path(start_url3, final_url3)
    #t1 = time.time()
    #write_to_file(out3, path3, t1-t0)

    #this one takes more time to finish then I have
    #path1 = shortest_path(start_url1, final_url1)
    #print(path1, len(path1))
    t0 = time.time()
    path2 = shortest_path(start_url2, final_url2)
    t1 = time.time()
    write_to_file(out2, path2, t1-t0)
