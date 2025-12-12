# CSVAnalyzer — USAGE

## Installation
pip install -r requirements.txt

## Utilisation
from csv_analyser import CSVAnalyser

an = CSVAnalyser("data.csv")
an.head(5)
sub = an.filter("gender", "female")
print(sub.mean("math score"))

## Features
- filter()
- sum()
- mean()
- sort()
- export JSON
- Logger

## Exemples
an = CSVAnalyser("data.csv")
sub = an.sort("math score", reverse=True)
sub.to_json("output.json")

