"""
quick and dirty count of the tests run in nightly regression

usage:
    python regression_count.py [report-url]

        Tests passed: 461, Tests failed: 0, Total Tests: 461

        Tests passed: 13, Tests failed: 0, Total Tests: 13
"""

from bs4 import BeautifulSoup
import requests
import sys


table_rows_in = lambda url: _get_parsed_page(url).find('table').findAll('tr')

def _get_parsed_page(link):
    '''
    provide regression report link, returns the BS object
    '''
    page = requests.get(link).text
    return BeautifulSoup(page)


def get_top_level_links(parent_link):
    '''
    returns a generator of tuples containing link and contents
    from the 'top level' of SEG/MVM links
    '''
    soup = _get_parsed_page(parent_link)
    return ((link.attrs, link.contents) for link in soup.findAll('a'))


def parse_index(html_page):
    '''
    returns a generator of links from the analysis page
    '''
    table_cells_in = lambda x: x.findAll('td')
    get_href_from = lambda x: x.find('a')['href']
    
    return (get_href_from(table_cells_in(tr)[2]) \
            for tr in table_rows_in(html_page) \
            if len(table_cells_in(tr)) == 5 \
            and "analysis" \
            in table_cells_in(tr)[2].text)


def parse_summary(link):
    '''
    returns a tuple of the tests passed/failed/total
    scraped from the summary pane
    '''
    # we only want the first row of the summary table
    summary = table_rows_in(link)[0].text.split()
    total_tests, tests_failed = int(summary[2]), int(summary[5])
    tests_passed = total_tests - tests_failed
    return(tests_passed, tests_failed, total_tests)


def aggregate_report(parent_link):
    '''
    print the final counts for the regression report to the console
    ex.
       Tests passed: 64, Tests failed: 6, Total Tests: 70
    '''
    for link, contents in get_top_level_links(parent_link):
        url = parent_link + link.popitem()[1]
        summary_url = lambda link: parent_link + contents[0] + '/' + link
        totals = (parse_summary(summary_url(i)) for i in parse_index(url))
        passed, failed, total = (sum(items) for items in zip(*totals))
        print("\n Tests passed: {}, Tests failed: {}, Total Tests: {}").format(
            passed, failed, total)

if __name__ == "__main__":
    # super jank
    if sys.argv[1].endswith('/'):
        aggregate_report(sys.argv[1])
    else:
        aggregate_report(sys.argv[1] + '/')        
