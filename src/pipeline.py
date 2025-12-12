import csv
from typing import List, Dict, Any
import math
import json
from datetime import datetime

#Lecture du fichier
def lire_csv(path: str) -> List[Dict[str,str]]:
	with open(path, newline ='', encoding = 'utf-8') as f:
		reader = csv.DictReader(f)
		return [row for row in reader]

#resume du fichier
def resume(data: List[Dict[str,str]], n: int = 3) -> None:
	if not data:
		print("Aucune donnée !")
		return
	cols = list(data[0].keys())
	print(f"Total lignes: {len(data)}")
	print(f"Colonnes: {cols}")
	print(f"Premières {n} lignes: ")
	for row in data[:3]:
		print(row)

#Filtrage
def filtrer(data: List[Dict[str, str]], colonne: str, valeur: str):
	return [row for row in data if row.get(colonne) == valeur]

#Convertir les nombres
def to_numbers(data: List[Dict[str,str]], colonne: str) -> float:
	nums = []
	for r in data:
		v = r.get(colonne, "")
		try:
			nums.append(float(v))
		except(ValueError, TypeError):
			continue
	return nums

# Calcul de la somme 
def somme(data: List[Dict[str, str]], colonne: str) -> float:
 	nums = to_numbers(data, colonne)
 	return sum(nums)

# FOnction calcul de la moyenne
def moyenne(data: List[Dict[str,str]], colonne: str) -> float:
	nums = to_numbers(data, colonne)
	return sum(nums) / len(nums) if nums else 0.0

#Autre fonction flexible
def statistique_flexible(data:List[Dict[str, str]] , *colonnes, arrondi: int=2, **options):
	resultat = {}
	#*colonnes est un tuple donc parcourir tuples
	for col in colonnes:
		s = somme(data, col)
		m = moyenne(data, col)
		resultat[col] = {"somme": round(s, arrondi), "moyenne": round(m, arrondi)}
	#**options est sous forme de dico
	if options.get("afficher", True):
		for col, stats in resultat.items():
			print(f"{col}: somme = {stats["somme"]}, moyenne= {stats["moyenne"]}")
	return resultat


	#✨Création de la calsse CSVAnalyser (POO)

class CSVAnalyser:
	#constrcteur
	def __init__(self, path: str = None, data: List[Dict[str, str]] = None, log_file: str = "csv_analyser.log"):
		if path: 
			self.data = lire_csv(path)
			self.path = path
		else:
			self.data = data or []
			self.path = None
		self.historique = []
		self.log_file = log_file

	#methode magique
	def __repr__(self):
		return f"CSVAnalyser(path = {self.path}, rows = {len(self.data)})"

	

	# Méthode qui ecrit un log et dans l'historique
	def log_writer(self, message: str):
		"""
		Ecrit dans le fichier log et l'historique

		"""
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		log_mess = f"[{timestamp}] {message}"
		self.historique.append(log_mess)
		with open(self.log_file, "w", encoding ="utf-8") as f:
			f.write(log_mess + "\n")

	# Méthode pour afficher historique
	def show_history(self):
		for i, op in enumerate(self.historique):
			print(f"{i}: {op}")

	# Méthode pour Trier
	def sort(self, colonne: str, reverse: bool=False):
		if not self.data:
			return CSVAnalyser(data=[])
		if colonne not in self.data[0]:
			raise ValueError(f"Colonne '{colonne}' inexistante")

		sorted_data = sorted(self.data, key=lambda r: float(r[colonne]) if r.get(colonne) else float('-inf'), reverse=reverse)
		new_analyzer = CSVAnalyser(data=sorted_data)
		self.log_writer(f"sort({colonne}, reverse={reverse})")
		return new_analyzer

	# Methode pour lise csv robuste
	def lire_csv_robuste(self, path:str):
		import csv
		self.invalide_lines = []
		valid_rows = []
		with open(path, newline='', encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for i, row in enumerate(reader, start = 1):
				try:
					valid_rows.append(row)
				except Exception as e:
					self.invalide_lines.append((i, str(e)))
		self.data=valid_rows
		self.path = path
		self.log_writer(f"Load CSV robuste: {len(valid_rows)} valides, {len(self.invalide_lines)} invalides")


	#Methode pour filter
	def filter(self, colonne: str, valeur: str):
		new_data = filtrer(self.data, colonne, valeur)
		new_analyzer = CSVAnalyser(data=new_data)
		self.log_writer(f"filter({colonne}=={valeur})")
		# new_analyzer.add_history(f"filter({colonne}=={valeur})")
		return new_analyzer

	#Méthode pour faire la somme
	def sum(self, colonne: str) -> float:
		val = somme(self.data, colonne)
		self.log_writer(f"sum({colonne})={val}")
		return val

	#Méthode pour calculer la moyenne
	def mean(self, colonne: str) -> float:
		val = moyenne(self.data, colonne)
		self.log_writer(f"mean({colonne})={val}")
		return val

	#Statistiques avancés
	def min_value(self, colonne: str):
		nums = [float(r[colonne]) for r in self.data if r.get(colonne)]
		return min(nums) if nums else None

	def max_value(self, colonne: str):
		nums = [float(r[colonne]) for r in self.data if r.get(colonne)]
		return max(nums) if nums else None

	def variance(self, colonne):
		nums = [float(r[colonne]) for r in self.data if r.get(colonne)]
		n = len(nums)
		if n < 2:
			return 0.0
		mean = sum(nums) / n
		return sum((x - mean) ** 2 for x in nums) / (n - 1)

	def std_dev(self, colonne):
		return math.sqrt(self.variance(colonne))

	#Méthode pour un resumé
	def head(self, n: int=5):
		resume(self.data, n)

	# Export en json
	def to_json(self, path:str):
		"""
		Exporte self.data dans un fichier JsON.
		Ajoute un log dans self.historique.
		"""

		try:
			with open(path, "w", encoding="utf-8") as f:
				json.dump(self.data, f, indent=4)
			desc = f"Export JSON vers {path} à {datetime.now()}"
			self.historique.append(desc)
			print(desc)
			return True
		except Exception as e:
			print(f"Erreur export JSON: {e}")
			return False

#Sous-classes
class StudentsAnalyser(CSVAnalyser):
	def moyenne_math(self):
		return self.mean("math score")
	def taux_reussite(self, seuil = 50):
		nums = to_numbers(self.data, "math score")
		if not nums: return 0.0
		passed = sum(1 for r in self.data if float(r.get("math score")) >= seuil)
		return passed / len(nums) * 100

if __name__ == "__main__":
	# data= lire_csv("../Data/StudentsPerformance.csv")
	# print(f"lignes lues:{len(data)} \n Première ligne: {data[-1]}")
	# resume(data)
	# femmes = filtrer(data, "gender", "female")
	# print(femmes[:3])
	# print(f"Somme math score : {somme(data, "math score")}")
	# print(f"Moyenne math score : {moyenne(data, "math score")}")
	# statistique_flexible(data, "math score", "reading score", "writing score", arrondi=3, afficher=False)
	an = CSVAnalyser("../Data/StudentsPerformance.csv")
	# print(an)
	# an.head()
	# sub = an.filter("gender", "female")
	# an.show_history()
	# print(sub)
	# print("Moyenne math (sub):", sub.mean("math score"))
	# an.show_history()
	an.lire_csv_robuste("../Data/StudentsPerformance.csv")
	sub = an.sort("math score", reverse=True)
	# sub.head(5)

	# st = StudentsAnalyser(data=an.data)
	# print(st.moyenne_math(), st.taux_reussite())
	# subf = st.filter("gender", "female")
	# print("Moyenne math (sub):", subf.mean("math score"))
	# st.show_history()
