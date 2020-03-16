import sys
import csv
import re
import math
from itertools import combinations, permutations
from string import punctuation

# Get User Input
input_filename = sys.argv[1]
output = sys.argv[2]
min_support_percentage = sys.argv[3]
min_confidence = sys.argv[4]

with open(input_filename) as f:
    read_content = f.readlines()
    print('Read Content from input file: ', read_content)

result = ''.join(i for i in read_content if not i.isdigit())
output = re.sub(r'\d+', '', result)
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

no_punctuations = ""
for char in output:
    if char not in punctuations:
        no_punctuations = no_punctuations + char

letters_arr = []

for c in no_punctuations:
    if c not in letters_arr:
        letters_arr.insert(len(letters_arr), c)

letters_arr.remove('\n')

comb_arr = []
for i in range(len(letters_arr)):
    if i is not 0:
        for p in combinations(letters_arr, i):
            comb_arr.insert(len(comb_arr), p)

vs_arr = []
for line in no_punctuations.splitlines():
    vs_arr.insert(len(vs_arr), line)

calc = {}
for line in vs_arr:
    print('Line: ', line)
    line_size = len(line)
    print('Line Size: ', line_size)
    for k in comb_arr:
        against = 0
        sizeK = len(k)
        if sizeK <= line_size:
            for c in k:
                if c in line:
                    against += 1

            if against == sizeK:
                add = "".join([str(c) for c in k])
                if add not in calc:
                    calc[add] = 1
                elif add in calc:
                    calc[add] += 1
print('Calc: ', calc)

# Generate Output file
output_filename = 'output.sup=%s,conf=%s.csv' % (
    min_support_percentage, min_confidence)
with open(output_filename, 'w') as out_file:
    write_output = csv.writer(out_file, quoting=csv.QUOTE_NONE, escapechar=' ')

    a = {}
    for i in calc:
        support_percentage = float(calc[i]/float(len(vs_arr)))
        if support_percentage >= float(min_support_percentage):
            i = sorted(i)
            i = str(i)
            i = i.translate(None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')
            a[i] = support_percentage
            (support_percentage) = '%.4f' % (support_percentage)
            print('Support Pct %s %s', support_percentage, i)
            y = ",".join(map(str, i))
            print('y: ', y)
            write_output.writerow(['S'] + [str(support_percentage)] + [y])

    catchDouble = []
    for i in a:
        if len(i) > 1:
            for p in permutations(i):
                add = "".join([str(c) for c in p])
                len_add = len(add)
                part = math.floor(float(len_add)/2)
                items1 = (add[0:int(part)])
                items2 = (add[int(part):int(len_add)])
                items1 = sorted(items1)
                items2 = sorted(items2)
                items1 = str(items1)
                items2 = str(items2)
                items1 = items1.translate(
                    None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')
                items2 = items2.translate(
                    None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')
                comb_items = items1 + '.' + items2
                comb_items2 = items2 + '.' + items1
                part2 = math.ceil(float(len_add) / 2)
                items3 = (add[0:int(part2)])
                items3 = sorted(items3)
                items3 = str(items3)
                items3 = items3.translate(
                    None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')
                items4 = (add[int(part2):int(len_add)])
                items4 = sorted(items4)
                items4 = str(items4)
                items4 = items4.translate(
                    None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')
                comb_items3 = items3 + '.' + items4
                comb_items4 = items4 + '.' + items3
                if items1 in a:
                    if items2 in a:
                        if i in a:
                            if comb_items not in catchDouble:
                                left = a[i] / a[items1]
                                if left >= float(min_confidence):
                                    left = '%.4f' % left
                                    (support_percentage) = '%.4f' % (a[i])
                                    x = ",".join(map(str, items1))
                                    y = ",".join(map(str, items2))
                                    write_output.writerow(
                                        ['R'] + [str(support_percentage)] + [str(left)] + [x] + ["'=>'"] + [y])
                                catchDouble.append(comb_items)
                            if comb_items2 not in catchDouble:
                                right = a[i] / a[items2]
                                if right >= float(min_confidence):
                                    right = '%.4f' % right
                                    (support_percentage) = '%.4f' % (a[i])
                                    x = ",".join(map(str, items1))
                                    y = ",".join(map(str, items2))
                                    write_output.writerow(
                                        ['R'] + [str(support_percentage)] + [str(right)] + [y] + ["'=>'"] + [x])
                                catchDouble.append(comb_items2)
                            if comb_items3 not in catchDouble:
                                if items3 in a:
                                    left2 = a[i] / a[items3]
                                    if left >= float(min_confidence):
                                        left2 = '%.4f' % left2
                                        (support_percentage) = '%.4f' % (a[i])
                                        x = ",".join(map(str, items3))
                                        y = ",".join(map(str, items4))
                                        write_output.writerow(
                                            ['R'] + [str(support_percentage)] + [str(left2)] + [x] + ["'=>'"] + [y])
                                        catchDouble.append(comb_items3)

                            if comb_items4 not in catchDouble:

                                if items4 in a:
                                    right2 = a[i] / a[items4]

                                    if right2 >= float(min_confidence):
                                        (support_percentage) = '%.4f' % (a[i])
                                        x = ",".join(map(str, items3))
                                        y = ",".join(map(str, items4))

                                        right2 = '%.4f' % right2
                                        write_output.writerow(
                                            ['R'] + [str(support_percentage)] + [str(right2)] + [y] + ["'=>'"] + [x])
                                        catchDouble.append(comb_items4)
