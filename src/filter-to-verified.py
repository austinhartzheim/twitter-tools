#! /usr/bin/env python3
import csv
import argparse

import libs.headers


def convert_files(in_reader, out_writer):
    '''
    :param in_reader: the input CSV reader.
    :param out_writer: the output CSV writer.
    '''
    first_row = True
    for row in in_reader:
        # Check if the first row is the header. If it is, we don't need to
        # write it again.
        if first_row:
            first_row = False
            if set(row.keys()) == set(libs.headers.full):
                continue

        if row['verified'] == 'True':
            out_writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('w'))
    args = parser.parse_args()

    in_reader = csv.DictReader(args.infile, libs.headers.full)
    out_writer = csv.DictWriter(args.outfile, libs.headers.full)
    out_writer.writeheader()

    convert_files(in_reader, out_writer)
