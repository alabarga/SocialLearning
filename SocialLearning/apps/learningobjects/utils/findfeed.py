#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup as bs4
import requests
import feedparser
import urllib.parse

# http://nombredelblog.blogspot.com/feeds/posts/default?alt=rss

def findfeed(site):
    raw = requests.get(site).text
    result = []
    possible_feeds = []
    html = bs4(raw)
    feed_urls = html.findAll("link", rel="alternate")
    if len(feed_urls) > 1:
        for f in feed_urls:
            t = f.get("type",None)
            if t:
                if "rss" in t or "xml" in t:
                    href = f.get("href",None)
                    if href:
                        possible_feeds.append(href)
    parsed_url = urllib.parse.urlparse(site)
    base = parsed.scheme+"://"+parsed_url.hostname
    atags = html.findAll("a")
    for a in atags:
        href = a.get("href",None)
        if href:
            if "xml" in href or "rss" in href or "feed" in href:
                possible_feeds.append(base+href)
    for url in list(set(possible_feeds)):
        f = feedparser.parse(url)
        if len(f.entries) > 0:
            if url not in result:
                result.append(url)
    return(result)