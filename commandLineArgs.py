import argparse

#Create command-line parser and parse agrs
def handleCommandLineArgs():
    parser = argparse.ArgumentParser(description='Run a Volumes Report')
    parser.add_argument('-f', '--file', help='Import file name')
    parser.add_argument('-m','--month', help='Volumes for desired month')
    parser.add_argument('-y', '--year', help='Volumes for desired year')
    parser.add_argument('-a', '--all', help='Volumes for all years')
    parser.add_argument('-d', '--dates', help='Volumes for date range')
    parser.add_argument('-t', '--format', help='Set the output file format (PDF, CSV')
    parser.add_argument('-o', '--outfile', help='Set output file name')
    args = parser.parse_args()
    return args