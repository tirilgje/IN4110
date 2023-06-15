import requests as req


def get_html(url, params=None, output=None):

    '''
    Makes a request for a url from a given website. Optionally take in parameters that are passed to the get function.

    Arguments:
        url (str): The url to get the html content from
        params (dict) [optional, default=None]: parameters passed to the function
        output (str) [optional, default=None]: name of the outputfile

    Returns:
        r.text (str): The html content

    '''
    if not isinstance(url, str):
        raise TypeError('url must be a string')

    r = req.get(url, params=params)

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
            f.write(r.url)
            f.write('\n\n')
            f.write(r.text)

    return r.text

if __name__ == '__main__':

    path = 'requesting_urls/'

    get_html('https://en.wikipedia.org/wiki/Studio_Ghibli', output = path + 'Studio_Ghibli.txt')


    get_html('https://en.wikipedia.org/wiki/Star_Wars', output = path + 'Star_Wars.txt')

    params = {'title':'Main_Page', 'action':'info'}
    get_html('https://en.wikipedia.org/w/index.php', params = params, output = path + 'index.txt')
