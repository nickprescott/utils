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


def _get_parsed_page(link):
    '''
    provide regression report link, returns the BS object
    '''
    page = requests.get(link).text
    soup = BeautifulSoup(page)
    return soup


def get_top_level_links(parent_link):
    '''
    returns a list of tuples containing link and contents
    from the 'top level' of SEG/MVM links
    '''
    soup = _get_parsed_page(parent_link)
    href = []
    for link in soup.findAll('a'):
        href.append((link.attrs, link.contents))
    return href


def parse_index(html_page):
    '''
    returns a list of links from the analysis page
    '''
    soup = _get_parsed_page(html_page)
    table = soup.find('table')
    rows = table.findAll('tr')
    links = []
    for table_row in rows:
        cols = table_row.findAll('td')
        if len(cols) == 5 and "analysis" in cols[2].text:
            link = cols[2].find('a')['href']
            links.append(link)
    return links


def parse_summary(link):
    '''
    returns a tuple of the tests passed/failed/total
    scrapes from the summary pane
    '''
    soup = _get_parsed_page(link)
    table = soup.find('table')
    row = table.find('tr')
    summary = row.text.split()
    total_tests = int(summary[2])
    tests_failed = int(summary[5])
    tests_passed = int(total_tests) - int(tests_failed)
    return(tests_passed, tests_failed, total_tests)


def aggregate_report(parent_link):
    '''
    outputs the finals counts for the regression report to the console
    ex.
       Tests passed: 64, Tests failed: 6, Total Tests: 70
    '''
    for link, contents in get_top_level_links(parent_link):
        url = parent_link + link.popitem()[1]
        analysis_links = parse_index(url)
        totals = []
        for link in analysis_links:
            url = parent_link + contents[0] + '/' + link
            totals.append(parse_summary(url))

        # totals is a list of tuples (pass, fail, skip) for each test scraped:
        # [(1-P, 11-F, 111-S), (2-P, 22-F, 222-S), (3-P, 33-F, 333-S)]
        #
        # zip(*totals) results in:
        # [(1-P, 2-P, 3-P), (11-F, 22-F, 33-F), (111-S, 222-S, 333-S)]
        #
        # representing a collection of each type (passed, failed, total)
        # which sum can iterate => [6-P, 66-F, 666-S]

        passed, failed, total = (sum(items) for items in zip(*totals))
        print("\n Tests passed: {}, Tests failed: {}, Total Tests: {}").format(
            passed, failed, total)

if __name__ == "__main__":
    # since we don't sanitize or verify trailing slashes...
    if sys.argv[1][-1] != '/':
        aggregate_report(sys.argv[1] + '/')
    else:
        aggregate_report(sys.argv[1])
