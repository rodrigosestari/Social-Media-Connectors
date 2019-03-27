#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Andrea Esuli (andrea@esuli.it)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import csv
import hashlib
import json
import logging
import os
import sys
import time

import feedparser
import requests

ENTRY_LINK = 'link'
URL = 'url'
CATS = 'cats'
SOURCE = 'source'

HTML_EXT = '.html'
JSON_EXT = '.json'


def load_feed_list(filenames):
    feeds = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                if len(row) > 2:
                    url = row[0]
                    source = row[1]
                    cats = row[2:]
                    feeds.append({URL: url, SOURCE: source, CATS: cats})
    return feeds


def download(feeds=None, pause=2, output_path='.'):
    count = 0
    logger = logging.getLogger(sys.argv[0])
    if feeds is None:
        feeds = []

    for feed in feeds:
        logger.info('Feed: ' + feed[URL])
        parsed_feed = feedparser.parse(feed[URL])
        if parsed_feed['bozo']:
            logger.error('Feed error: ' + str(parsed_feed['bozo_exception']))

        for entry in parsed_feed.entries:
            try:
                logger.info('Link: ' + entry[ENTRY_LINK])
            except KeyError as ke:
                logger.error('Link error: ' + str(ke))
                continue
            filename = hashlib.sha256(entry[ENTRY_LINK].encode()).hexdigest()
            missing = False
            for cat in feed[CATS]:
                fullname = os.sep.join([output_path, feed[SOURCE], cat, filename])
                if not os.path.exists(fullname + HTML_EXT):
                    missing = True
                    break
            if not missing:
                logger.info('Already downloaded')
                continue

            try:
                resp = requests.get(entry[ENTRY_LINK])
            except requests.RequestException as re:
                logger.error('Link error: ' + str(re))
                continue

            count += 1
            html = resp.content

            for cat in feed[CATS]:
                dirname = os.sep.join([output_path, feed[SOURCE], cat])
                try:
                    os.makedirs(dirname, exist_ok=True)
                    fullname = os.sep.join([dirname, filename])
                    with open(fullname + HTML_EXT, 'wb') as out:
                        out.write(html)
                    with open(fullname + JSON_EXT, 'w', encoding='utf-8') as out:
                        json.dump(entry, out)
                    logger.info('Saved to ' + fullname)
                except IOError as ioe:
                    logger.error('Save error: ' + str(ioe))
            time.sleep(pause)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--pause', help='Pause in seconds between URL get requests', type=int, default=2)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('output_path', help='Path where to save the downloaded content', type=str)
    parser.add_argument('feeds', help='CSV file listing URLs of RSS feeds and the assigned categories', type=str,
                        nargs='+')
    args = parser.parse_args()

    logger = logging.getLogger(sys.argv[0])
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.info('Verbose output')

    feeds = load_feed_list(args.feeds)

    count = download(feeds, args.pause, args.output_path)
    logger.info('%d pages downloaded.' % count)
