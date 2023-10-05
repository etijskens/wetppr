#!/usr/bin/env python

# a little script to sort the output of hello-mpi-omp.slurm jobs

import sys

if __name__ =='__main__':
    filename = sys.argv[1]
    print(f"sorting {filename}...\n")
    with open(filename) as f:
        all_lines = f.readlines()
    lines = []
    for line in all_lines:
        if line.startswith('Host='):
            lines.append(line[:-1])
    lines.sort()
    for line in lines:
        print(line)