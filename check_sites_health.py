import argparse
from collections import OrderedDict
from datetime import datetime
import re
import urllib

import requests
from whois import whois


def get_urls_location_from_terminal():
    parser = argparse.ArgumentParser()
    parser.add_argument("sites_list_filepath", help="Sites list location", type=str)
    args = parser.parse_args()
    return args.sites_list_filepath

def load_urls(filepath):
    with open(filepath, 'r') as text_file:
        text = text_file.read()
    return re.findall(r'.+', text)

def prettify_urls(urls):
    urls = ['http://{}'.format(u) if not re.match(r'https?://', u) else u for u in urls]
    return set(urls)

def get_http_status_code(url):
    request_timeout = 5
    try:
        request = requests.get(url, timeout=request_timeout)
    except (requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout,
            requests.packages.urllib3.exceptions.ReadTimeoutError,
            requests.exceptions.ReadTimeout):
        return  
    else:
        return request.status_code

def get_domain_expiration_date(domain_name):
    domain = whois(domain_name)
    expiration_date = domain.expiration_date
    if isinstance(expiration_date, list):
        expiration_date = expiration_date[0]
    if isinstance(expiration_date, str):
        date_format = "%Y-%m-%dT%H:%M:%S.0Z"
        expiration_date = datetime.strptime(expiration_date, date_format)
    return expiration_date

def extract_domain(url):
    if url.endswith('gov.ru'):
        return 'gov.ru'
    elif url.endswith('edu.ru'):
        return 'edu.ru'
    else:
        return urllib.parse.urlparse(url).netloc


def get_days_until_expiration(expiration_date):
    now = datetime.now()
    return max((expiration_date - now).days, 0)

def is_remained_time_more_than_month(days_until_expiration):
    days_in_month = 30
    return days_until_expiration > 30

def get_info_about_status_code(status_code):
    if status_code:
        verdict = ('OK' if (status_code == 200) else 'WARNING!')
        return 'HTTP status code: {}({})'.format(status_code, verdict)
    else:
        return 'Failed to get HTTP status code.'

def get_info_about_expiration_date(expiration_date):
    if expiration_date:
        days_until_expiration = get_days_until_expiration(expiration_date)
        verdict = ('OK' 
                    if is_remained_time_more_than_month(days_until_expiration)
                    else 'WARNING!')
        return 'Days until expiration date: {}({})'.format(
                    days_until_expiration,
                    verdict)
    else:
        return 'Failed to get domain expiration date.'

def get_url_info(url):
    status_code = get_http_status_code(url)
    exp_date = get_domain_expiration_date(extract_domain(url)) \
                      if status_code else None
    return {'status code':get_info_about_status_code(status_code),
            'expiration date':get_info_about_expiration_date(exp_date)}


def main():
    urls_location = get_urls_location_from_terminal()
    urls = prettify_urls(load_urls(urls_location))
    for index, url in enumerate(urls, 1):
        print('{}) {}'.format(index, url))
        url_info = get_url_info(url)
        print(' • {}'.format(url_info['status code']))
        print(' • {}'.format(url_info['expiration date']))


if __name__ == '__main__':
    main()



