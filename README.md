
# firefox-bookmarks-merger

Tool for merging firefox bookmarks backups. Designed for people who don't want to use cloud based tools like firefox sync, plugins, want to version control their bookmarks backups or have any other reason to do this locally.
Fork from original repository: https://github.com/james-cube/firefox-bookmarks-merger.git

## Usage

### How to backup/restore firefox bookmarks?

In top menu `Bookmarks` under `Show All Bookmarks` there is button `Import and Backup` which allows you to perform those operations either using `json` or `html` file. This module uses and generates `json` backups. 

### How to use the tool?

#### Listing bookmarks

Writes simple tree structure of one or more files as text format, showing all firefox bookmarks in menu, toolbar and starred.
Tree structures of several input files can be written into a single output files or into several ones
separately. If no output file is given, one is created automatically.


`python bookmarks_merger --list --files tests/testcase1.json`
`python bookmarks_merger --list --files tests/testcase1.json --output testcase1.txt`
`python bookmarks_merger --list --files tests/testcase1.json tests/testcase2.json --output testcases.txt`
`python bookmarks_merger --list --files tests/testcase1.json tests/testcase2.json --output testcase1.txt testcase2.txt` 

[Example output](https://github.com/parasange/firefox-bookmarks-merger/blob/master/tests/expected/testcase1_tree_to_file_expected.txt)

#### Cleaning bookmarks or folders

Cleans one or more files from duplicated bookmarks and folders. Duplicated bookmarks are deleted, that one with last
modified date is kept. Duplicated folders are merged into a single one. Output files are of .json format.
If no output file is given, one or more are created automatically.

`python bookmarks_merger --clean --files tests/testcase1.json`
`python bookmarks_merger --clean --files tests/testcase1.json --output tests/testcase1_cleaned.json`
`python bookmarks_merger --clean --files tests/testcase1.json tests/testcase2.json --output tests/testcase1_cleaned.json tests/testcase2_cleaned.json`



#### Merge

Merges two or more files into one single file. First one is considered "primary". Bookmarks from next files will be appended.
There is no removal of duplicated bookmarks and folders.
If no output file is given, one is created automatically.

`python bookmarks_merger --merge --files tests/testcase1.json tests/testcase2.json`
`python bookmarks_merger --merge --files tests/testcase1.json tests/testcase2.json --output tests/testcases_merged.json`


#### Merge and clean

Merges two or more files into one single file and removes duplicated bookmarks and folders. Duplicated bookmarks are deleted, that one with last
modified date is kept. Duplicated folders are merged into a single one. Output files are of .json format.
If no output file is given, one is created automatically.

`python bookmarks_merger --merge --clean --files tests/testcase1.json tests/testcase2.json`
`python bookmarks_merger --merge --clean --files tests/testcase1.json tests/testcase2.json --output tests/testcases_merged.json`

#### (Sort)

Not implemented yet.
Sort folders and/or bookmark titles alphabetically.

### All program arguments

```
usage: firefox_bookmarks_merger [-h] (--list | --clean | --merge (--clean))
                                --files FILES [FILES ...] --output OUTPUT [OUTPUTS ...]

optional arguments:
  -h, --help            show this help message and exit
  --list                Write all titles and urls of all bookmarks to text file
  --clean               Remove duplicated bookmarks and merge duplicated folders
  --merge               Merge bookmarks into one file
  --merge --clean       Merge bookmarks into one file, remove duplicated bookmarks and merge duplicated folders
  --files FILES [FILES ...]
                        List of input file(s) to process
  --output OUTPUT [OUTPUTS ...]       
                        Output file(s)
```