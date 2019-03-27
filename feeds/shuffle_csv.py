import argparse
import csv
import random

MY_LARGE_FIELD = 1024 * 1024 * 100

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('input', help='input csv file', type=str)
    parser.add_argument('output', help='output csv file', type=str)
    args = parser.parse_args()

    if csv.field_size_limit() < MY_LARGE_FIELD:
        csv.field_size_limit(MY_LARGE_FIELD)

    with open(args.input, mode='r', encoding='utf-8') as inputfile:
        reader = csv.reader(inputfile)
        data = [(random.random(), row) for row in reader]
    data.sort()
    with open(args.output, mode='w', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        for _, row in data:
            writer.writerow(row)
    print('Processed '+ str(len(data)) + ' rows.')
