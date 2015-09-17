import os
import re
import csv
import sys
import bisect
from collections import Counter
from statistics import StatisticsError


class WordCounter:
    def __init__(self, infolder='wc_input', outfolder='wc_output',
                       med_outfile='med_result.txt', wc_outfile='wc_result.txt'):
        self.infolder, self.outfolder, self.med_outfile, self.wc_outfile = infolder, outfolder, med_outfile, wc_outfile
        self.counts = Counter()
        self.line_lengths = []
        self.infiles = sorted(os.listdir(infolder))

    def _clean(self, line):
        # removes hyphens and apostrophes
        incoming_string = re.sub('[-\'_]', '', line)

        # replaces all other nonalphanumeric characters with spaces
        incoming_string = re.sub('[^a-zA-Z0-9_]', ' ', incoming_string)

        return incoming_string.lower().split()

    def _presorted_median(self, xs):
        n = len(xs)
        if n == 0:
            raise StatisticsError('no median for empty data')
        if n % 2 == 1:
            return xs[n // 2]
        else:
            i = n // 2
            return (xs[i - 1] + xs[i]) / 2

    def read_all(self):
        for fname in self.infiles:
            with open(os.path.join(self.infolder, fname)) as f:
                for line in f:
                    words_in_line = self._clean(line)
                    self.counts.update(words_in_line)
                    self.line_lengths.append(len(words_in_line))

    def write_counts(self):
        with open(os.path.join(self.outfolder, self.wc_outfile), 'w') as d:
            writer = csv.writer(d, delimiter='\t')
            for word, count in sorted(self.counts.items()):
                writer.writerow([word, str(count)])

    def write_median(self):
        sorted_lengths = []
        with open(os.path.join(self.outfolder, self.med_outfile), 'w') as f:
            for linelength in self.line_lengths:
                bisect.insort(sorted_lengths, linelength);
                f.write('{0:.1f}\n'.format(self._presorted_median(sorted_lengths)))

    def run(self):
        self.read_all()
        self.write_counts()
        self.write_median()

if __name__ == '__main__':
    WordCounter(*sys.argv[1:]).run()
