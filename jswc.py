#!/usr/bin/env python
import argparse, httplib2
import threading

import sys
from bs4 import BeautifulSoup, SoupStrainer
from urlparse import urlparse


def parse_href(a_tag, url):
    link_found = None
    href = a_tag.attrs['href']
    if href != "#" and "javascript" not in href and "mailto:" not in href:
        if (href.startswith(url.scheme)):
            link_found = urlparse(href)
        elif href.startswith("/"):
            link_found = urlparse(url.scheme + "://" + url.netloc + href)
        else:
            link_found = urlparse(url.scheme + "://" + url.netloc + "/" + href)
    return link_found


def get_links(base_url, url):
    links = []
    if base_url.netloc == url.netloc:
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        status, response = http.request(url.geturl())
        if status.status == 200 and "image" not in status['content-type']:
            for a_tag in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
                if a_tag.has_attr('href'):
                    link = parse_href(a_tag, url)
                    if link:
                        links.append(link)
    return links


def worker(base, url, crawled):
    for link in get_links(base, url):
        if link not in crawled:
            crawled.append(link)
            threading.Thread(target=worker, args=(base, urlparse(link.geturl()), crawled,)).start()
            sys.stdout.write("[+] " + link.geturl() + "\n")
            sys.stdout.flush()
    return


if __name__ == '__main__':
    crawled = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="The URL to scan.")
    args = parser.parse_args()
    if args.url:
        base_url = urlparse(args.url)
        try:
            http = httplib2.Http(disable_ssl_certificate_validation=True)
            status, response = http.request(base_url.geturl())
            sys.stdout.write("\n======================================================")
            sys.stdout.write("\nSERVER: " + status['server'])
            sys.stdout.write("\nX-POWERED-BY: " + status['x-powered-by'])
            sys.stdout.write("\n======================================================\n")
            base = []
            for link in get_links(base_url, base_url):
                base.append(link)
            for url in base:
                threading.Thread(target=worker, args=(base_url, url, crawled,)).start()
        except httplib2.ServerNotFoundError as e:
            sys.stdout.write(e.message + "\n")
            sys.stdout.flush()
