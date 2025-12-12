import pytest
from csv_analyser import CSVAnalyser

def test_sum_mean():
    data = [{"val": "10"}, {"val": "20"}, {"val": "30"}]
    an = CSVAnalyser(data=data)
    assert an.sum("val") == 60
    assert an.mean("val") == 20

def test_filter():
    data = [{"col": "A"}, {"col": "B"}, {"col": "A"}]
    an = CSVAnalyser(data=data)
    sub = an.filter("col", "A")
    assert len(sub.data) == 2

def test_sort():
    data = [{"x": "3"}, {"x": "1"}, {"x": "2"}]
    an = CSVAnalyser(data=data)
    sub = an.sort("x")
    assert [float(r["x"]) for r in sub.data] == [1,2,3]

def test_to_json(tmp_path):
    data = [{"a":1}]
    an = CSVAnalyser(data=data)
    path = tmp_path / "out.json"
    assert an.to_json(path)
    assert path.exists()