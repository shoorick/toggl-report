#!/usr/bin/env python

import argparse
import pandas as pd
import re
import sys


def parse_arguments():
    """
    Parse command line arguments or print usage information
    """
    parser = argparse.ArgumentParser(description='Combine Toggl report with issues list')
    parser.add_argument('-s', '--summary',
                        help='read summary report from file',
                        default='')
    parser.add_argument('-t', '--time',
                        help='read time entries from file',
                        default='')
    parser.add_argument('-i', '--issues',
                        help='issues list',
                        default='')
    parser.add_argument('-f', '--filter',
                        help='filter input file by column=value',
                        default='')
    parser.add_argument('-o', '--output',
                        help='output to file',
                        default='')
    return parser.parse_args()


def main():
    """
    Parse arguments, read, combine and output the data
    """
    args = parse_arguments()

    if args.summary:
        summary = pd.read_csv(args.summary)
        summary['Duration'] = pd.to_timedelta(summary['Duration'])
    elif args.time:
        entries = pd.read_csv(args.time)
        entries['Duration'] = pd.to_timedelta(entries['Duration'])
        summary = entries.groupby('Description')['Duration'].sum().reset_index()
    else:
        sys.exit('Specify --summary or --time input file.\nUse -h or --help to get usage help.')

    if args.issues:
        issues = pd.read_csv(args.issues)
    else:
        sys.exit('Specify --issues input file.\nUse -h or --help to get usage help.')

    output = args.output
    if output and not re.search(r'\.(csv|html?|js(on)?|xlsx)$', output, re.I):
        sys.exit(f'Output file {output} has unknown type. '
            + 'Only CSV, HTML, JSON and XSLX are available.\n')

    if args.filter:
        column, value = args.filter.split('=')
        if column in summary and value:
            summary = summary.loc[summary[column] == value]

    if not 'Description' in summary:
        sys.exit('No Description column in report file')
    if not 'Issue' in issues:
        sys.exit('No Issue column in issues list')

    # Convert types to make comparison possible
    summary['Issue'] = pd.to_numeric(
        summary['Description'].str.extract(r'#(\d+)', expand=False),
        errors='coerce').astype('Int16')
    issues['Issue'] = pd.to_numeric(issues['Issue'], errors='coerce').astype('Int16')
    issues['Ready'] = issues['Ready'] == 1

    merged = pd.merge(summary, issues, on='Issue', how='outer')
    filtered = merged[['Issue', 'Title', 'Comment', 'Duration']]

    if output:
        if re.search(r'\.csv$', output, re.I):
            filtered.to_csv(output, index=False)
        elif re.search(r'\.html?$', output, re.I):
            filtered.to_html(output, index=False)
        elif re.search(r'\.js(on)?$', output, re.I):
            filtered.to_json(output, index=False)
        elif re.search(r'\.xlsx$', output, re.I):
            filtered.to_excel(output, index=False)
    else:
        filtered.to_csv(sys.stdout, index=False)

if __name__ == '__main__':
    main()
