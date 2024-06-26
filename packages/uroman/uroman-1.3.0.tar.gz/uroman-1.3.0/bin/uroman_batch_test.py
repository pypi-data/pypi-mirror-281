#!/usr/bin/env python3

import argparse
# from collections import defaultdict
import datetime
import os
from pathlib import Path
import regex
import sys
from typing import Optional, Tuple


default_test_dir = '/Users/ulf2/projects/NLP/uroman/test-large'
default_data_dir = '/nas/home/ulf/romanizer/data'
src_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(src_dir)
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "test-large")


def slot_value_in_double_colon_del_list(line: str, slot: str, default: Optional = None) -> Optional[str]:
    """For a given slot, e.g. 'cost', get its value from a line such as '::s1 of course ::s2 ::cost 0.3' -> 0.3
    The value can be an empty string, as for ::s2 in the example above."""
    m = regex.match(fr'(?:.*\s)?::{slot}(|\s+\S.*?)(?:\s+::\S.*|\s*)$', line)
    return m.group(1).strip() if m else default


def load_iso_8859_1(filename: str) -> dict:
    n_entries = 0
    d = {}  # key: tuple(str, str)  value: list[lang_names] or lang_group
    with open(filename) as f_in:
        for line in f_in:
            if line.startswith('#'):
                continue
            lcode = slot_value_in_double_colon_del_list(line, 'lang-code')
            lang_name_s = slot_value_in_double_colon_del_list(line, 'lang-names')
            lang_group = slot_value_in_double_colon_del_list(line, 'lang-group')
            if lcode:
                if lang_name_s:
                    lang_names = regex.split(r'[;,]\s*', lang_name_s)
                    d[('names', lcode)] = lang_names
                    n_entries += 1
                if lang_group:
                    d[('group', lcode)] = lang_group
                # print('    FF', lcode, lang_names, lang_group)
    sys.stderr.write(f'Read in {n_entries} entries from {filename}\n')
    return d


def diff_files(file1, file2, space_norm: bool) -> Tuple[int, int, int, int]:
    n_lines_identical = 0
    n_lines_different = 0
    with open(file1) as f1:
        with open(file2) as f2:
            lines1 = f1.read().rstrip().split('\n')
            lines2 = f2.read().rstrip().split('\n')
            n1_overage = overage if ((overage := len(lines1) - len(lines2)) > 0) else 0
            n2_overage = overage if ((overage := len(lines2) - len(lines1)) > 0) else 0
            for line1, line2 in zip(lines1, lines2):
                if space_norm:
                    line1 = regex.sub(r' +', ' ', line1)
                    line2 = regex.sub(r' +', ' ', line2)
                    line1 = regex.sub(r'^\s*', '', line1)
                    line2 = regex.sub(r'^\s*', '', line2)
                if line1 == line2:
                    n_lines_identical += 1
                else:
                    n_lines_different += 1
    return n_lines_identical, n_lines_different, n1_overage, n2_overage


def batch_romanize(new_version_id: str, args, large_test_dir: Path = default_test_dir):
    n_files = 0
    n_imperfect_files = 0
    n_lines = 0
    lang_code_dict = load_iso_8859_1(f'{data_dir}/ISO-639-3-list.txt')
    combination_outfile = f"{large_test_dir}/combination.v{new_version_id}.html"
    combination_logfile = f"{large_test_dir}/combination.v{new_version_id}.log.txt"
    with open(combination_outfile, 'w') as f_comb_html, open(combination_logfile, 'w') as f_comb_log:
        for file in sorted(os.listdir(large_test_dir)):
            filename = os.fsdecode(file)
            if m := regex.match(r'([a-z]{3})(\.braille|).txt$', filename):
                lcode, braille = m.group(1, 2)
                lang_names = lang_code_dict[('names', lcode)]
                # lang_group = lang_code_dict[('group', lcode)]
                # print(f"{new_version_id} {lcode}: {', '.join(lang_names)} ({lang_group}) {filename}")
                n_files += 1
                in_file = f"{test_dir}/{filename}"
                out_file = f"{test_dir}/{lcode}{braille}.v{new_version_id}.txt"
                curr_file = f"{test_dir}/{lcode}{braille}.curr.txt"
                if not Path(out_file).is_file():
                    ablation_clause = f' -a "{ablation}"' if (ablation := args.ablation) else ''
                    command = f"uroman.py -i {in_file} -o {out_file} --lcode {lcode} --silent{ablation_clause}"
                    if n_files > 2:
                        print(f"uroman {lcode}{braille}")
                    else:
                        print(command, '  ', lang_names[0])
                    if exit_code := os.system(command):
                        print(f'Exception ({exit_code}) in command: {command}')
                        return
                if Path(out_file).is_file():
                    n_same, n_diff, n1_over, n2_over = diff_files(curr_file, out_file, True)
                    # print(f"{out_file} already exists for {lcode} ({lang_names[0]}) w/ {n_same} matching lines")
                    if n_diff or n1_over or n2_over:
                        message = f"diff {lcode}{braille}  ={n_same}, {n_diff*'*'}{n_diff}, {n1_over}, {n2_over} " \
                                  f"({lang_names[0]})"
                        print(message)
                        f_comb_log.write(message + '\n')
                        f_comb_log.flush()
                        html_file = f"{test_dir}/{lcode}{braille}.v{new_version_id}.html"
                        if not Path(html_file).is_file():
                            col_command = (f"color-mt-diffs.pl {curr_file} {out_file} {in_file} -l perl python ref "
                                           f"-o {html_file} -s --silent")
                            if lcode in ['bod', 'dzo''']:
                                col_command += ' -m'  # ignore middle dots (used as Tibetan syllable separators)
                            if n_files <= 2:
                                print(col_command, '  ', lang_names[0])
                            os.system(col_command)
                        with open(html_file) as f_lang_html:
                            n_imperfect_files += 1
                            phase = 'head'
                            for line in f_lang_html:
                                if (phase == 'head') and (n_imperfect_files == 1):
                                    f_comb_html.write(line)
                                    n_lines += 1
                                if regex.match(r'\s*</body', line):
                                    phase = 'tail'
                                if phase == 'body':
                                    f_comb_html.write(line)
                                    n_lines += 1
                                if regex.match(r'\s*<body.*>', line):
                                    phase = 'body'
                                    diff_len_clause = f' &nbsp; n1-over: {n1_over} n2-over: {n2_over}' \
                                                      f'{diff_len_clause}\n' \
                                        if n1_over or n2_over else ""
                                    f_comb_html.write(f'<p>\n<h1>{lcode}{braille} '
                                                      f'({lang_names[0]}) {n_diff}/{n_diff+n_same}'
                                                      f'{diff_len_clause}</h1>\n')
                                    n_lines += 1
        f_comb_html.write('  </body>\n</html>\n')
        sys.stderr.write(f'Combined {n_imperfect_files} html files into {combination_outfile} with {n_lines} lines.\n)')
    sys.stderr.write(f'Processed {n_files} files.\n')


def compare_series(version1_id: str, version2_id: str, large_test_dir: Path = default_test_dir):
    n_files = 0
    n_imperfect_files = 0
    n_lines = 0
    lang_code_dict = load_iso_8859_1(f'{data_dir}/ISO-639-3-list.txt')
    combination_outfile = f"{large_test_dir}/combination.diff.v{version1_id}-v{version2_id}.html"
    with open(combination_outfile, 'w') as f_comb_html:
        for file in sorted(os.listdir(large_test_dir)):
            filename = os.fsdecode(file)
            if m := regex.match(r'([a-z]{3})(\.braille|)\.v(.*)\.txt$', filename):
                lcode, braille, version = m.group(1, 2, 3)
                if version != version1_id:
                    continue
                lang_names = lang_code_dict[('names', lcode)]
                # lang_group = lang_code_dict[('group', lcode)]
                ref_file = f"{test_dir}/{lcode}{braille}.txt"
                file1 = f"{test_dir}/{lcode}{braille}.v{version1_id}.txt"
                file2 = f"{test_dir}/{lcode}{braille}.v{version2_id}.txt"
                n_files += 1
                if Path(file1).is_file() and Path(file2).is_file():
                    n_same, n_diff, n1_over, n2_over = diff_files(file1, file2, True)
                    if n_diff or n1_over or n2_over:
                        print(f'diff {lcode}  ={n_same}, *{n_diff}, {n1_over}, {n2_over}')
                        html_file = f"{test_dir}/{lcode}{braille}.diff.v{version1_id}-v{version2_id}.html"
                        if not Path(html_file).is_file():
                            col_command = (f"color-mt-diffs.pl {file1} {file2} {ref_file} "
                                           f"-l {version1_id} {version2_id} ref "
                                           f"-o {html_file} -s --silent")
                            if lcode in ['bod', 'dzo']:
                                col_command += ' -m'  # ignore middle dots (used as Tibetan syllable separators)
                            print(col_command, '  ', lang_names[0])
                            os.system(col_command)
                        with open(html_file) as f_lang_html:
                            n_imperfect_files += 1
                            phase = 'head'
                            for line in f_lang_html:
                                if (phase == 'head') and (n_imperfect_files == 1):
                                    f_comb_html.write(line)
                                    n_lines += 1
                                if regex.match(r'\s*</body', line):
                                    phase = 'tail'
                                if phase == 'body':
                                    f_comb_html.write(line)
                                    n_lines += 1
                                if regex.match(r'\s*<body.*>', line):
                                    phase = 'body'
                                    diff_len_clause = f' &nbsp; n1-over: {n1_over} n2-over: {n2_over}' \
                                                      f'{diff_len_clause}\n' \
                                        if n1_over or n2_over else ""
                                    f_comb_html.write(f'<p>\n<h1>{lcode} ({lang_names[0]}) {n_diff}/{n_diff+n_same}'
                                                      f'{diff_len_clause}</h1>\n')
                                    n_lines += 1
        f_comb_html.write('  </body>\n</html>\n')
        sys.stderr.write(f'Combined {n_imperfect_files} html files into {combination_outfile} with {n_lines} lines.\n)')
    sys.stderr.write(f'Processed {n_files} files.\n')

# uroman_batch_test.py -v 1.3.0
# uroman_batch_test.py -r 1.3.0.11 -v 1.3.0.12
# uroman_batch_test.py -r 1.3.0.12 -v 1.3.0.13
# uroman_batch_test.py -v 1.3.0.13 -a nocap


def main():
    start_time = datetime.datetime.now()
    print(f"Start time: {start_time:%A, %B %d, %Y at %H:%M}")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_filename', type=Path)
    parser.add_argument('-r', '--ref_version', type=Path)
    parser.add_argument('-v', '--new_version', type=Path)
    parser.add_argument('-a', '--ablation', type=str)
    args = parser.parse_args()
    if args.ref_version and args.new_version:
        compare_series(str(args.ref_version), str(args.new_version), Path(default_test_dir))
    else:
        batch_romanize(args.new_version, args, Path(default_test_dir))


if __name__ == "__main__":
    main()
