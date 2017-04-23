#!/usr/bin/env python
import argparse, httplib2, sys

from bs4 import BeautifulSoup, SoupStrainer
from urlparse import urlparse

if __name__ == '__main__':
    crawled = []
    emails = []
    to_crawl = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="The URL to scan.")
    parser.add_argument("--file", help="The output file to save results.")
    args = parser.parse_args()
    if args.url:
        url = urlparse(args.url)
        to_crawl.append(url.geturl())
        while len(to_crawl) > 0:
            sys.stdout.write("\r" + str(len(to_crawl)))
            sys.stdout.flush()
            try:
                crawling = to_crawl.pop()
                if crawling not in crawled:
                    http = httplib2.Http(disable_ssl_certificate_validation=True)
                    status, response = http.request(crawling)
                    for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
                        if link.has_attr('href'):
                            if "mailto:" in link['href']:
                                emails.append(link['href'].replace("mailto:", ""))
                            elif link['href'] != "#" and link['href'] != "/" and "javascript" not in link['href']:
                                arg = None
                                if (link['href'].startswith(url.scheme)):
                                    arg = urlparse(link['href'])
                                else:
                                    if link['href'].startswith("/"):
                                        arg = urlparse(url.scheme + "://" + url.netloc + link['href'])
                                    else:
                                        if link['href'].startswith("http"):
                                            arg = urlparse(link['href'])
                                        else:
                                            path = url.geturl().split("/")
                                            arg = urlparse(url.geturl().replace(path[len(path) - 1], "") + link['href'])
                                if arg.netloc == url.netloc:
                                    url_found = arg.geturl()
                                    if url_found not in crawled:
                                        if url_found not in to_crawl:
                                            to_crawl.append(url_found)
                    crawled.append(crawling)
            except:
                pass
        if args.file:
            file = open(args.file, 'w')
            for link in crawled:
                file.write("%s\n" % link)
            file.close()
        else:
            for link in crawled:
                print link
