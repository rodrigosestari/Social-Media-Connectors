import argparse
import logging
import os
import re
import shutil
import sys

from feed_extractor import TEXT_EXT
from feed_monitor import JSON_EXT

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j', '--json', help='Also copy the JSON file', action='store_true')
    parser.add_argument('-o', '--overwrite', help='Overwrite if already extracted', action='store_true')
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('input_dir', type=str, help='Path to directory where html from feeds, with metadata, is saved')
    parser.add_argument('output_dir', type=str,
                        help='Path to directory where the extracted text, with metadata, will be saved')
    parser.add_argument('filter_file', type=str,
                        help='File with regular expressions to filter out text when a match is found. One regex per line.')
    args = parser.parse_args()

    logger = logging.getLogger(sys.argv[0])
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.info('Verbose output')

    regexs = list()
    with open(args.filter_file, 'r', encoding='utf8') as regexfile:
        for line in regexfile:
            regexs.append(re.compile(line.strip()))

    for root, dirs, files in os.walk(args.input_dir):
        for file in files:
            if file.endswith(TEXT_EXT):
                output_dir = os.path.join(args.output_dir, root[len(args.input_dir):])
                output_file = os.path.join(output_dir, file)
                if not os.path.exists(output_file) or args.overwrite:
                    os.makedirs(output_dir, exist_ok=True)
                    filename = os.path.join(root, file)
                    with open(filename, encoding='utf8', mode='r') as inputfile:
                        with open(output_file, encoding='utf8', mode='w') as outputfile:
                            for line in inputfile:
                                for regex in regexs:
                                    line = regex.sub(' ', line)
                                line = line.strip()
                                if len(line) > 0:
                                    outputfile.write(line)
                                    outputfile.write('\n')
                    logger.info('Processed ' + filename)
                else:
                    logger.info('Skipping ' + file)
            if file.endswith(JSON_EXT) and args.json:
                output_dir = os.path.join(args.output_dir, root[len(args.input_dir) + 1:])
                output_file = os.path.join(output_dir, file)
                if not os.path.exists(output_file) or args.overwrite:
                    os.makedirs(output_dir, exist_ok=True)
                    shutil.copyfile(os.path.join(root, file), output_file)
