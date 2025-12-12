import os
import pytest
import sys

# Ajouter Src/ au PYTHONPATH pour que Python trouve pipeline.py
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
from pipeline import CSVAnalyser


def test_to_json(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    an = CSVAnalyser(data=data)
    
    assert an.to_json(file_path) == True
    assert os.path.exists(file_path)
    
    # Vérifier que le fichier contient bien le JSON
    import json
    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == data
    # Vérifier historique

    assert len(an.historique) == 1
