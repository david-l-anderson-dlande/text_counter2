import os
import re
import csv
import sys
import bisect
import statistics
from collections import Counter


def wc_m_main(input_folder='wc_input', output_folder='wc_output',
              med_out_file='med_result.txt', wc_out_file='wc_result.txt'):
    linelengths, fulldict, files_list = _initializer(input_folder)
    linelengths, fulldict = file_reader(linelengths, fulldict,
                                        files_list, input_folder)
    count_writer(output_folder, wc_out_file, fulldict)
    median_writer(output_folder, med_out_file, linelengths)


def _initializer(input_folder_i):
    line_length_list = []
    dictionary_initializer = Counter()
    input_files_list = sorted(os.listdir(input_folder_i))
    return line_length_list, dictionary_initializer, input_files_list


def file_reader(linelengths_fr, fulldict_fr, files_list_fr, input_folder_fr):
    for file in files_list_fr:
        with open(os.path.join(input_folder_fr, file), 'r') as f:
            for line in f:
                line_list = _cleaner_lister(line)
                linelengths_fr.append( len(line_list) )
                fulldict_fr.update(line_list)
    return linelengths_fr, fulldict_fr


def _cleaner_lister(incoming_string):
    incoming_string = re.sub('[-\'_]', '', incoming_string)
    #removes hyphens and apostrophes
    incoming_string = re.sub('[^a-zA-Z0-9_]', ' ', incoming_string)
    #replaces all other nonalphanumeric characters with spaces
    incoming_string = incoming_string.lower()
    outgoing_list = incoming_string.split()
    return outgoing_list


def count_writer(output_folder, wc_out_file, fulldict_cw):
    with open(os.path.join(output_folder, wc_out_file), 'w') as d:
        writer = csv.writer(d, delimiter='\t')
        for word, count in sorted(fulldict_cw.items()):
            writer.writerow([word, str(count)])


def median_writer(output_folder, med_out_file, linelengths_mw):
    sorted_list = []
    with open(os.path.join(output_folder, med_out_file), 'w') as m:
        for linelength in linelengths_mw:
            bisect.insort(sorted_list, linelength)
            m.write('{0:.1f}\n'.format( _presorted_median(sorted_list) ) )


def _presorted_median(data):
    n = len(data)
    if n == 0:
        raise statistics.StatisticsError('no median for empty data')
    if n % 2 == 1:
        return data[n // 2]
    else:
        i = n // 2
        return (data[i - 1] + data[i]) / 2


if __name__ == '__main__':
    wc_m_main(*sys.argv[1:])
