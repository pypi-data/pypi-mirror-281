#!/usr/bin/env python3

from collections import defaultdict
import os
import regex
import sys
from typing import Optional

src_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(src_dir)
data_dir = os.path.join(root_dir, "data")


def slot_value_in_double_colon_del_list(line: str, slot: str, default: Optional = None) -> Optional[str]:
    """For a given slot, e.g. 'cost', get its value from a line such as '::s1 of course ::s2 ::cost 0.3' -> 0.3
    The value can be an empty string, as for ::s2 in the example above."""
    m = regex.match(fr'(?:.*\s)?::{slot}(|\s+\S.*?)(?:\s+::\S.*|\s*)$', line)
    return m.group(1).strip() if m else default


def load_unicode_script_names(filename: str) -> dict:
    d = defaultdict(int)
    n_entries = 0
    with open(filename) as f_in:
        for line in f_in:
            if line.startswith('#'):
                continue
            if m := regex.search(r'\s;\s+(\S+)\s+\#', line):
                script_name_with_underscores = m.group(1)
                script_name = script_name_with_underscores.replace('_', ' ')
                script_name = script_name.replace('Canadian Aboriginal', 'Canadian Syllabics')
                script_name = script_name.replace('Meroitic Hieroglyphs', 'Meroitic Hieroglyphic')
                script_name = script_name.replace('Hieroglyphs', 'Hieroglyph')
                # noinspection SpellCheckingInspection
                script_name = script_name.replace('Phags Pa', 'Phags-Pa')
                # noinspection SpellCheckingInspection
                script_name = script_name.replace('Cypro Minoan', 'Cypro-Minoan')
                d[script_name] += 1
                n_entries += 1
    sys.stderr.write(f'Read in {n_entries} entries with {len(d)} unique scripts from {filename}\n')
    return d


def load_script_names(filename: str = 'Scripts.txt') -> dict:
    d = defaultdict(int)
    n_entries = 0
    with open(filename) as f_in:
        for line in f_in:
            if line.startswith('#'):
                continue
            if script_name := slot_value_in_double_colon_del_list(line, 'script-name'):
                d[script_name] += 1
                n_entries += 1
    sys.stderr.write(f'Read in {n_entries} entries with {len(d)} unique scripts from {filename}\n')
    return d


def diff_scripts(unicode_data_script_d: dict, script_d: dict) -> None:
    n_missing, n_spurious = 0, 0
    for script_name in sorted(unicode_data_script_d):
        if script_name not in script_d:
            print(f'::script-name {script_name}')
            n_missing += 1
    print()
    for script_name in sorted(script_d):
        if script_name not in unicode_data_script_d:
            print(f'{script_name} only in Scripts.txt')
            n_spurious += 1
    print(f'{n_missing} entries missing, {n_spurious} spurious')


def main():
    script_d = load_script_names(f'{data_dir}/Scripts.txt')
    unicode_data_script_d = load_unicode_script_names(f'{data_dir}/UnicodeDataScripts.txt')
    diff_scripts(unicode_data_script_d, script_d)


if __name__ == "__main__":
    main()
