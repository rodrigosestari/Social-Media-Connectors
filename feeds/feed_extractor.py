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
import logging
import os
import re
import shutil
import sys

import bs4
import chardet

from feed_monitor import HTML_EXT, JSON_EXT

TEXT_EXT = '.txt'


def visible(element):
    if element.parent.name in ['a', 'style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--separator', help='Separator between different pieces of extracted text', type=str,
                        default='\n')
    parser.add_argument('-j', '--json', help='Also copy the JSON file', action='store_true')
    parser.add_argument('-o', '--overwrite', help='Overwrite if already extracted', action='store_true')
    parser.add_argument('-m', '--min_length', help='Minimum length of text to be not filtered out', type=int,
                        default=25)
    parser.add_argument('-f', '--filter_out', help='Regex that matches any text to be removed', type=str)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('input_dir', type=str, help='Path to directory where html from feeds, with metadata, is saved')
    parser.add_argument('output_dir', type=str,
                        help='Path to directory where the extracted text, with metadata, will be saved')
    args = parser.parse_args()

    logger = logging.getLogger(sys.argv[0])
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.info('Verbose output')

    if args.filter_out:
        logger.info('Using filter regex: ' + args.filter_out)
        filter_out = re.compile(args.filter_out).search
    else:
        filter_out = lambda _: False

    for root, dirs, files in os.walk(args.input_dir):
        for file in files:
            if file.endswith(HTML_EXT):
                output_dir = os.path.join(args.output_dir, root[len(args.input_dir):])
                output_file = os.path.join(output_dir, file[:-len(HTML_EXT)] + TEXT_EXT)
                if not os.path.exists(output_file) or args.overwrite:
                    os.makedirs(output_dir, exist_ok=True)
                    with open(os.path.join(root, file), 'rb') as f:
                        guess = chardet.detect(f.read())
                    encoding = 'utf-8'
                    if guess is not None:
                        if guess['encoding'] is not None:
                            encoding = guess['encoding']
                    html = ''
                    filename = os.path.join(root, file)
                    with open(filename, encoding=encoding, errors='ignore') as f:
                        html = f.read()
                    html = re.sub('\s+', ' ', html)
                    soup = bs4.BeautifulSoup(html, 'html.parser')
                    all_text = soup.findAll(text=True)
                    extracted_text = args.separator.join([i.strip() for i in filter(visible, all_text) if
                                                          len(i) > args.min_length and not filter_out(i)])
                    logger.info('Extracted %d chars from %s (%s)' % (len(extracted_text), filename, encoding))
                    with open(output_file, 'w', encoding='utf-8', errors='ignore') as out:
                        out.write(extracted_text)
                else:
                    logger.info('Skipping ' + file)
            if file.endswith(JSON_EXT) and args.json:
                output_dir = os.path.join(args.output_dir, root[len(args.input_dir) + 1:])
                output_file = os.path.join(output_dir, file)
                if not os.path.exists(output_file) or args.overwrite:
                    os.makedirs(output_dir, exist_ok=True)
                    shutil.copyfile(os.path.join(root, file), output_file)
