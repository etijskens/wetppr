# -*- coding: utf-8 -*-

"""
Package mkdefs
=======================================

find all occurences of bold text in all .md files listed in mkdocs.yml. and the heading in which they appear
produce an alphabetic list of them and links to the heading

Run this script from the project directory:

```shell
(wiptools-py3.9) etijskens@MacOSX@local [511] ~/workspace/wetppr
> python make-glossary.py
```
"""

__version__ = "0.1.0"
# set to True for debugging
VERBOSE = False

from pathlib import Path
import re
from typing import Union
import yaml

def make_glossary( path_to_project: Path, md_files_to_ignore: list = [], out: str ='glossary.md', verbose: bool = False):
    """Extract a glossary from docs/*.md. Terms are assumed to be marked as '**Bold face text**'.
    For every term a link is created to the section in which the term is appearing. The links are
    nicely formatted in a glossary.md file.
    """
    path_to_project = Path(path_to_project)
    if not path_to_project.is_dir():
        raise FileNotFoundError(f"'{path_to_project}' is not a directory.")

    md_files_to_ignore.append(out)
    # md_files = list_docs(path_to_project / 'mkdocs.yml')
    md_files = (path_to_project / 'docs').glob('*.md')
    links = parse(md_files, md_files_to_ignore=md_files_to_ignore)
    lines = format_links(links)
    if verbose:
        for line in lines:
            print(line)

    with open(path_to_project / 'docs' / out, mode='w') as f:
        for line in lines:
            print(line, file=f)

def list_docs(path_to_mkdocs_yml: Union[str,Path]) -> list:
    """Read a mkdocs.yml file and return all files appearing under the 'nav:' entry.
    """
    # retrieve the filenames
    p = Path(path_to_mkdocs_yml)
    with open(p, "r") as f:
        yaml_data = yaml.safe_load(f)
    md_files = yaml_data['nav'] # a list of filenames

    # convert the filenames to filepaths
    p = p.parent / 'docs'
    if not p.is_dir():
        raise FileNotFoundError()
    for i, filename in enumerate(md_files):
        if isinstance(filename, dict):
            # sometimes a nav entry needs to show up differently: e.g.
            #   nav:
            #       Assignment: assignment-2022-23.md
            # these entries are turned into a dictionary: {'Assignment': 'assignment-2022-23.md'}
            # the following line extracts the filename from it:
            filename = list(filename.values())[0]
        md_files[i] = p / filename

    return md_files


def parse(filepaths, md_files_to_ignore=[]) -> list[str]:
    """Parse all filepaths not in ignore. Return a list of links."""
    links = []
    for p in filepaths:
        if not p.name in md_files_to_ignore:
            links.extend(parse_md(p))
    return links


def parse_md(file_md: Union[str,Path]) -> list:
    """Parse a .md file, looking for '**bold face text**', identifying a term,
    and the title of the paragraph in which the bold face text is found. The bold
    face text may span two lines.

    Return a list of markdown links in autorefs format:

        '[bold face text][title-of-the-section-in-which-the-bold-face-text-is-found]'
    """
    if VERBOSE:
        print(f"file={file_md}")
    with open(file_md,'r') as f:
        lines = f.readlines()
    current_title =  ''
    links = []
    l = 0
    line = lines[l]
    while l < len(lines):
        if line.startswith('#'):
            current_title = process_title(line)
            line_done = True
        elif line.startswith('```'):
            if VERBOSE:
                print(f"line={line}")
            # beginning of a code block. Skip lines until the end of the code block
            l += 1
            while not lines[l].startswith('```'):
                if VERBOSE:
                    print(f"line={lines[l]}",end='')
                l += 1
            line_done = True
        else:
            # look for "**<whatever>**"
            rex_bf  =   r'\*\*[^*]+\*\*'       #  '**blabla bla**'
            rex_bfs = r'\*\*\*[^*]+\*\*\*'     # '***blabla bla***'
            bf_terms  = re.findall(rex_bf , line)
            bfs_terms = re.findall(rex_bfs, line)
            for bf_term in bf_terms:
                if not f"*{bf_term}*" in bfs_terms:
                    links.append(f"[{bf_term[2:-2]}][{current_title}]")
                    line = line.replace(bf_term, '')
            # look for '**<wathever>$'
            rex_bf = r'\*\*.+$'
            bf_terms  = re.findall(rex_bf , line)   #  '**blabla'
            bfs_terms = re.findall(rex_bfs, line)   # '***blabla'
            line_done = True # most probably, will be unset if not
            for bf_term in bf_terms:
                if not f"*{bf_term}" in bfs_terms:
                    term0 = bf_term.strip()[2:]
                    # find the second part on the next line, otherwise ignore
                    l += 1
                    line = lines[l]
                    rex = r'^[^*]+\*\*'
                    bf_terms = re.findall(rex, line)
                    for bf_term in bf_terms:
                        term1 = bf_term.strip()[:-2]
                        links.append(f"[{term0} {term1}][{current_title}]")
                        line = line[len(bf_term):]
                        line_done = False
        if line_done:
            l += 1
            try:
                line = lines[l]
            except IndexError:
                pass
    return links


def process_title(line: str) -> str:
    """Take a text line with a title or subtitle, remove the leading '#'-characters, strip(), remove
    punctation and replace spaces with hyphens, convert to lowercase and return the resulting string.
    """
    while line[0] == '#':
        line = line[1:]
    line = line.strip()
    # remove punctuation:
    t = line
    for c in ".,?!'":
        t = t.replace(c, '')
    # replace spaces with hyphens
    t = t.replace(' ', '-')
    # convert to lowercase:
    t = t.lower()

    return t


def format_links(links: list[str]) -> list[str]:
    """Take a list of links, put them in alphabetical order, add a title, and subtitles A, B, C, ...
    Return a list of lines.
    """
    links = sorted(links, key=str.casefold)

    prev = ''
    lines = ["# Glossary"
            ,""
            ,"Here is an alphabetical list of terms with links to where they are explained in the text."
            ]


    for link in links:
        c = link[1].upper()
        if c != prev:
            prev = c
            lines.extend([ "", f"## {c}", ""])
        lines.append(f"- {link}")

    return lines

# Q&D testing: create a glossary for the wetppr project.
if __name__ == "__main__":
    make_glossary( Path.cwd()
                 , md_files_to_ignore = [
                        'index.md'
                      , 'about-the-author.md'
                      , 'overview.md'
                      , 'evaluation.md'
                      , 'assignment.md'
                      , "guide-lines.md"
                      , "links.md"
                      ]
                 , verbose=True)

    print("-*# finished #*-")
