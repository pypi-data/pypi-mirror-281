#!/usr/bin/env python3

import argparse
from collections import defaultdict
import regex
import sys
from typing import Optional


def slot_value_in_double_colon_del_list(line: str, slot: str, default: Optional = None) -> Optional[str]:
    """For a given slot, e.g. 'cost', get its value from a line such as '::s1 of course ::s2 ::cost 0.3' -> 0.3
    The value can be an empty string, as for ::s2 in the example above."""
    m = regex.match(fr'(?:.*\s)?::{slot}(|\s+\S.*?)(?:\s+::\S.*|\s*)$', line)
    return m.group(1).strip() if m else default


def decode_unicode_escapes(s: str) -> str:
    if regex.search(r'\\[xuU][0-9A-Fa-f]{2}', s):
        result = ''
        rest = s
        while m := regex.match(r'(.*?)(\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})(.*)$', rest):
            pre, core, rest = m.group(1, 2, 3)
            cp = int(core[2:], 16)
            # escape only for non-ASCII, specifically not for \x22, \x25 (quote, apostrophe)
            if cp > 0x80:
                result += pre + chr(cp)
            else:
                result += pre + core
        result += rest + ('\n' if s.endswith('\n') else '')
        return result
    else:
        return s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('direct_input', nargs='*', type=str)
    parser.add_argument('-i', '--input_filename', type=str, help='default: sys.stdin')
    parser.add_argument('-o', '--output_filename', type=str, help='default: sys.stdout')
    args = parser.parse_args()
    d_suffix_groups_per_lang = defaultdict(list)
    with open(args.input_filename) as f_in, open(args.output_filename, 'w') as f_out:
        line_number = 0
        for line in f_in:
            line_number += 1
            decode_unicode_escaped_line = decode_unicode_escapes(line)
            f_out.write(decode_unicode_escaped_line)
            if m := regex.match(r"::lc\s+(\S+)\s+::suffix-group\s+(\S.*\S)\s*$", decode_unicode_escaped_line):
                lang_code, group = m.group(1,2)
                d_suffix_groups_per_lang[lang_code].append(group)
        f_out.write("\n")
        for lang_code in sorted(d_suffix_groups_per_lang.keys()):
            f_out.write(f"{lang_code}: ({'); ('.join(d_suffix_groups_per_lang[lang_code])})\n")
    sys.stderr.write(f"{line_number} lines.\n")


if __name__ == "__main__":
    main()
