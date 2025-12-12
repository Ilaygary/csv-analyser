import csv
from typing import List, Dict, Any

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

#calcul de la moyenne
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
	def __init__(self, path: str = None, data: List[Dict[str, str]] = None):
		if path: 
			self.data = lire_csv(path)
			self.path = path
		else:
			self.data = data or []
			self.path = None
		self.historique = []

	#methode magique
	def __repr__(self):
		return f"CSVAnalyser(path = {self.path}, rows = {len(self.data)})"

	#Ajouter opération dans l'historique
	def add_history(self, desc: str):
		self.historique.append(desc)


	# Méthode pour afficher historique
	def show_history(self):
		for i, op in enumerate(self.historique):
			print(f"{i}: {op}")
	#Methode pour filter
	def filter(self, colonne: str, valeur: str):
		new_data = filtrer(self.data, colonne, valeur)
		new_analyzer = CSVAnalyser(data=new_data)
		self.add_history(f"filter({colonne}=={valeur})")
		# new_analyzer.add_history(f"filter({colonne}=={valeur})")
		return new_analyzer
	#somme
	def sum(self, colonne: str) -> float:
		val = somme(self.data, colonne)
		self.add_history(f"sum({colonne})={val}")
		return val

	#Méthode pour calculer la moyenne
	def mean(self, colonne: str) -> float:
		val = moyenne(self.data, colonne)
		self.add_history(f"mean({colonne})={val}")
		return val
	#Méthode pour un resumé
	def head(self, n: int=5):
		resume(self.data, n)

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

	st = StudentsAnalyser(data=an.data)
	print(st.moyenne_math(), st.taux_reussite())
	subf = st.filter("gender", "female")
	print("Moyenne math (sub):", subf.mean("math score"))
	st.show_history()
