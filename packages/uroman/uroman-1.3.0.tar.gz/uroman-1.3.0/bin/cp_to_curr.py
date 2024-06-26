#!/usr/bin/env python3

import argparse
import os
import shutil
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('version', type=str, help='e.g.: v1.3.0.12')
    parser.add_argument('-d', '--directory', type=str, default='.')
    args = parser.parse_args()
    n_entries = 0
    for version_file in sorted(os.listdir(args.directory)):
        if version_file.endswith(f".{args.version}.txt"):
            full_version_file = os.path.join(args.directory, version_file)
            current_file = version_file.replace(args.version, 'curr')
            full_current_file = os.path.join(args.directory, current_file)
            command = f"cp {full_version_file} {full_current_file}"
            sys.stderr.write(command + '\n')
            # shutil.copyfile(full_version_file, full_current_file)
            n_entries += 1
    sys.stderr.write(f"Copied {n_entries} entries.\n")


if __name__ == "__main__":
    main()
