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

def remove_subdomain(domain):
    domain_levels = domain.split('.')
    if len(domain_levels) > 1:
        return '.'.join(domain_levels[1:])

def prettify_expiration_date(exp_date):
    if isinstance(exp_date, list):
        exp_date = exp_date[0]
    if isinstance(exp_date, str):
        date_format = "%Y-%m-%dT%H:%M:%S.0Z"
        exp_date = datetime.strptime(exp_date, date_format)
    return exp_date

def get_domain_expiration_date(domain):
    domain_info = whois(domain)
    exp_date = domain_info.expiration_date
    if not exp_date:
        domain = get_rid_of_the_subdomain(domain)
        return (get_domain_expiration_date(domain) if domain else None)
    return prettify_expiration_date(exp_date)

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

def extract_domain(url):
    return urllib.parse.urlparse(url).netloc

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



