from pipeline import CSVAnalyser

an = CSVAnalyser("../Data/StudentsPerformance.csv")
print("Min math score:", an.min_value("math score"))
print("Max math score:", an.max_value("math score"))
print("Variance math score:", an.variance("math score"))
print("Écart-type math score:", an.std_dev("math score"))

success = an.to_json("students_export.json")
print("Export réussi ?", success)
print("Historique :", an.historique[:3])