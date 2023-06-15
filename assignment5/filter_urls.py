import re
from requesting_urls import get_html

def find_urls(html_string, base_url=None, output=None):
    '''
    Find all urls in a html string

    Arguments:
        html_string (str): the html text
        base_url (str) [optional, default=None]: the base url
        output (str) [optional, default=None]: name of the ouputfile
    Returns:
        url_list (list): list of all urls in the html text
    '''
    #find all anchor-tags including href
    anchors = re.findall("<a.*href=\".*\".*>", html_string)
    # make it a string again
    anchors = '\n'.join(anchors)
    # want to find on the content between 'href="' and '"' or '#'
    matches = re.findall("(?<=href=\")[/h].+?(?=[\"#])", anchors)

    #handle partial urls
    if base_url is not None:
        if not isinstance(base_url, str):
            raise TypeError('base_url must be a string')

        #urls that starts with '// should have 'https:'' added
        #urls that starts with '/' should have base_url added if given
        for i, match in enumerate(matches):
            if match.startswith('//'):
                matches[i] = 'https:' + match
            elif match.startswith('/'):
                matches[i] = base_url + match
    else:
        #urls that starts with '// should have 'https:'' added
        for i, match in enumerate(matches):
            if match.startswith('//'):
                matches[i] = 'https:' + match

    #using set to exclude identical matches
    url_list = list(set(matches))

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
            for url in url_list:
                f.write(url + '\n')

    return url_list

def find_articles(html_string, base_url=None, output=None, en_only=False):
    '''
    Find all article urls in a html string

    Arguments:
        html_string (str): the full html text
        base_url (str) [optional, default=None]: the base url
        output (str) [optional, default=None]: name of the ouputfile
        en_only (bool) [optional, default=False]: if true, the function only finds articles from the english wikipedia

    Returns:
        article_url_list (list): list of all urls that are articles
    '''

    urls = find_urls(html_string, base_url=base_url)
    urls = '\n'.join(urls)

    if en_only:
        pattern = r'^https?:\/\/en\.wikipedia\.[a-z]{2,3}/wiki/[^:]+$'
    else:
        pattern = r'^https?:\/\/[a-z]{2}\.wikipedia\.[a-z]{2,3}/wiki/[^:]+$'

    article_url_list = re.findall(pattern, urls,flags=re.MULTILINE)

    if output is not None:

        if not isinstance(output, str):
            raise TypeError('output must be a string')

        if output.find('.') > 0:
            filename, ext = output.split('.')
            if ext != '.txt':
                ext = '.txt'
            output_filename = filename + ext
        else:
            output_filename = output + '.txt'

        with open(output_filename, 'w') as f:
            for url in article_url_list:
                f.write(url + '\n')

    return article_url_list


def test_find_urls():
    '''
    Small test for the find_urls function
    '''
    html = """
    <a href="#fragment-only">anchor link</a>
    <a id="some-id" href="/relative/path#fragment">relativelink</a>
    <a href="//other.host/same-protocol">same-protocol link</a>
    <a href="https://example.com">absolute URL</a>
    """
    urls = find_urls(html, base_url ="https://en.wikipedia.org")
    assert set(urls) == set(["https://en.wikipedia.org/relative/path",
    "https://other.host/same-protocol", "https://example.com"])


if __name__ == '__main__':

    test_find_urls()

    test_urls = ['https://en.wikipedia.org/wiki/Nobel_Prize',
                 'https://en.wikipedia.org/wiki/Bundesliga',
                 'https://en.wikipedia.org/wiki/2019-20_FIS_Alpine_Ski']


    outputs = ['Nobel_Prize', 'Bundesliga', '2019-20_FIS_Alpine_Ski']

    base_url = 'https://en.wikipedia.org'
    path = 'filter_urls/'

    for url, out in zip(test_urls, outputs):
        html_string = get_html(url)
        all_urls = find_urls(html_string, base_url=base_url, output=path + out)
        article_urls = find_articles(html_string, base_url=base_url, output=path + 'articles_' + out)
        print(path+out, len(all_urls), len(article_urls))
