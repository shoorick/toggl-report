# CLI tools to process Toggl reports

## Preparing

```bash
make prepare
. venv/bin/activate
```
or
```bash
sudo apt install pip3-venv
python3 -m venv env
. venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Combine Toggl report with issues list by issue number

```bash
combine.py [-h] [-s SUMMARY] [-t TIME] [-i ISSUES] [-f FILTER] [-o OUTPUT]
```

Issue numbers extracted from `Description` columns of summary files
and compared with `Issue` column of issue list.

### Optional arguments

* `-h`, `--help` — show help message and exit
* `-s` _SUMMARY_, `--summary` _SUMMARY_ — read summary report from file
* `-t` _TIME_, `--time` _TIME_ — read time entries from file
* `-i` _ISSUES_, `--issues` _ISSUES_ — read issues list from file
* `-f` _FILTER_, `--filter` _FILTER_ — filter input file by `column=value`
* `-o` _OUTPUT_, `--output` _OUTPUT_ — output to file

Any of _SUMMARY_ or _TIME_ is enough

#### File formats

Appropriate file format is choosing according to its
extension.

##### Both input and output

* CSV — Comma Separated Values — `file.csv`

##### Output only

* HTML — Hypertext Markup Language — `file.htm`, `file.html`
* JSON — JavaScript Notation Object — `file.json`, `file.js`
* Microsoft Excel — `file.xlsx`

## Examples

Read Track summary report, combine it with issue list `issues.csv`
and put the result to `merged.csv`

```bash
./combine.py -s Toggl_Track_summary_report_2023-03-01_2024-02-29.csv \
  -i issues.csv -o merged.csv
```

Filter input file by project name

```bash
./combine.py -s Toggl_Track_summary_report_2023-03-01_2024-02-29.csv \
  -f Project=Something \
  -i issues.csv -o merged.csv
```
