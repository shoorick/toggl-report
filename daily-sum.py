#!/usr/bin/env python3

import argparse
import pandas as pd
import sys

def duration_to_seconds(duration):
    '''Convert HH:MM:SS duration strings to integer seconds'''
    h, m, s = map(int, duration.split(':'))
    return h * 3600 + m * 60 + s


def seconds_to_duration(seconds):
    '''Convert integer seconds to HH:MM:SS string'''
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f'{h:02}:{m:02}:{s:02}'


def seconds_to_hours(seconds):
    '''Convert integer seconds amount to hours'''
    return seconds / 3600

def parse_arguments():
    """
    Parse command line arguments or print usage information
    """
    parser = argparse.ArgumentParser(description='Sum Toggl report entries daily')
    parser.add_argument('-i', '--input',
                        help='read time entries from file instead of standard input',
                        default='')
    parser.add_argument('-o', '--output',
                        help='output to file instead of standard output',
                        default='')
    parser.add_argument('-p', '--project',
                        help='group by project, ignore issue description',
                        action='store_true',
                        default=0)
                        
    return parser.parse_args()


def main():
    """
    Parse arguments, read, combine and output the data
    """
    args = parse_arguments()

    df = pd.read_csv(args.input if args.input else sys.stdin)

    df['Seconds'] = df['Duration'].apply(duration_to_seconds)

    columns = ['Project', 'Start date'] if args.project else ['Project', 'Description', 'Start date']
    grouped = df.groupby(columns)['Seconds'].sum().reset_index()
    grouped['Hours'] = grouped['Seconds'].apply(seconds_to_hours)
    grouped.drop(columns=['Seconds'], inplace=True)

    grouped.to_csv(args.output if args.output else sys.stdout, index=False)


if __name__ == '__main__':
    main()
