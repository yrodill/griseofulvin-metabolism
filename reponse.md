# Réponse aux questions :

## **Diapo 30**

***Dans ce petit modèle, quelles sont les réactions essentielles,
bloquées et alternatives ?***

- Essentielle(s) : R1 (à la fois valeur minimale et maximale)
- Bloquées : Aucune car il y a une valeur maximum pour toutes les réactions
- Alternatives : R2, R3 et R4 (possèdent une valeur max)

## **Diapo 31/32**

***Pour les 6 exemples suivants, vérifier si les molécules T sont productibles
à partir de S en prenant en compte la stœchiométrie (FBA) et sans la
prendre en compte (analyse de graphe). L’expliquer.***

```python
# coding: utf-8

from cobra import *

S = Metabolite(
        id = 'S',
        name = 'Seed metabolite',
	compartment="coucou")

C1 = Metabolite(
        id = 'C1',
        name = 'metabolite C1',
	compartment="coucou")

C2 = Metabolite(
        id = 'C2',
        name = 'metabolite C2',
	compartment="coucou")

T = Metabolite(
        id = 'T',
        name = 'Target metabolite',
	compartment="coucou")

reaction1 = Reaction(
	id = "r1", 
	name = "reaction 1",
	lower_bound = 0,
	upper_bound = 1000
)
reaction1.add_metabolites({
	S: -1,
        T: 1
})

reaction2 = Reaction(
	id = "r2", 
	name = "reaction 2",
	lower_bound = 0,
	upper_bound = 1000
)
reaction2.add_metabolites({
	S: -1,
        C1: -1,
        C2: 1
})

reaction3 = Reaction(
	id = "r3", 
	name = "reaction 3",
	lower_bound = 0,
	upper_bound = 1000
)
reaction3.add_metabolites({
	C2: -1,
        C1: 1
})

reaction4 = Reaction(
	id = "r4", 
	name = "reaction 4",
	lower_bound = 0,
	upper_bound = 1000
)
reaction4.add_metabolites({
	C2: -1,
        T: 1
})

reaction5 = Reaction(
	id = "r5", 
	name = "reaction 5",
	lower_bound = 0,
	upper_bound = 1000
)
reaction5.add_metabolites({
	S: -1,
        C1: -1,
        T: 1
})

reaction6 = Reaction(
	id = "r6", 
	name = "reaction 6",
	lower_bound = 0,
	upper_bound = 1000
)
reaction6.add_metabolites({
	C2: -1,
        C1: 2
})

reaction7 = Reaction(
	id = "r7", 
	name = "reaction 7",
	lower_bound = 0,
	upper_bound = 1000
)
reaction7.add_metabolites({
	C2: -1,
        C1: 1,
        T: 1
})

reaction8 = Reaction(
	id = "r8", 
	name = "reaction 8",
	lower_bound = 0,
	upper_bound = 1000
)
reaction8.add_metabolites({
	S: -1,
        C1: -1,
        C2: 2
})

reaction9 = Reaction(
	id = "r9", 
	name = "reaction 9",
	lower_bound = 0,
	upper_bound = 1000
)
reaction9.add_metabolites({
	C2: -1,
        C1: 1,
})

reactionImp_S = Reaction(
        id = "import_S",
        name = "reaction import S",
        lower_bound = 0,
        upper_bound = 1000
)
reactionImp_S.add_metabolites({S:1})

reactionExp_T = Reaction(
        id = "export_T",
        name = "reaction export T (objective reaction)",
        lower_bound = 0,
        upper_bound = 1000
)
reactionExp_T.add_metabolites({T:-1})

# creating models
model_a = Model("Model_a")
model_a.add_reactions([reactionImp_S, reactionExp_T,reaction1])

model_b = Model("Model_b")
model_b.add_reactions([reactionImp_S, reactionExp_T,reaction2,reaction3,reaction4])

model_c = Model("Model_c")
model_c.add_reactions([reactionImp_S, reactionExp_T,reaction5])

model_d = Model("Model_d")
model_d.add_reactions([reactionImp_S, reactionExp_T,reaction2,reaction6, reaction4])

model_e = Model("Model_e")
model_e.add_reactions([reactionImp_S, reactionExp_T,reaction2,reaction7])

model_f = Model("Model_f")
model_f.add_reactions([reactionImp_S, reactionExp_T,reaction8,reaction9,reaction4])

def run(model):
	print("\n")
	print(str(model) + " : ")
	print("__________________ ")
	model.objective = "export_T"
	solution = model.optimize()
	fluxMax = solution.objective_value
	print("\n")
	print(fluxMax)

	# model.summary()

	solution = model.optimize()
	# flux contenus dans solutions.fluxes
	# for reac in model.reactions:
	# 	print(str(reac.id) + " : " + str(solution.fluxes[reac.id]))

	# FVA analyze flux
	FVA_result = flux_analysis.variability.flux_variability_analysis(model, fraction_of_optimum = 1.0)

	print("\n")
	print(FVA_result)
	print("\n")

run(model_a)
run(model_b)
run(model_c)
run(model_d)
run(model_e)
run(model_f)
```
*En prenant en compte la stoechiométrie* :

D'après les résultats obtenus avec le script on peut dire que les modèles b et c ne permettent pas de produire de molécule T. 
Le modèle d permet de produire du T mais avec un rendement moins bon.
Les autres modèles a,e et f permettent de créer du T.

*En analyse de graphe* :

On aurait tendance à dire que les modèles contenant des cyles ne peuvent pas produire de T. Par exemple pour la réaction r2 du modèle b, il faudrait un apport de C1 pour faire la réaction.

Le script calculant les flux semble permissif au niveau des cycles en permettant une réaction qui semble impossible en analyse de graphe.


## **Diapo 35**

***Faire tourner le modèle, et trouver une manière de représenter graphiquement le résultat obtenu. Et si on retire la réaction R01786 du modèle ?***

Si on retire R01786, le alpha-D-glucose n'est plus transporté, tous les flux sont divisés par 2 sauf pour le béta-d-glucose (création,transport) de la réaction R01600.

Pour représenter graphiquement le modèle on utilise la librairie cobrapy pour écrire un fichier xml (sbml) avec la ligne de commande suivante :

```python
cobra.io.write_sbml_model(modelWikipedia, "graphe_oriente.xml")
```

On ouvre ensuite ce le fichier .xml avec cytoscape. On modifie le layout pour avoir une représentation plus lisible.

**Voir fichier en pièce jointe graphe.xgmml**

## **Diapo 37**

***Nombre de réactions, de métabolites, de gènes. Nombre de réactions et de métabolites partagés. Différences dans la composition de biomasse. Étude de flux dans ces deux modèles. Soyez inventifs !***

- E.coli : **2583** réactions, **1805** métabolites, **1367** gènes.
- Salmonella : **2546** réactions, **1802** métabolites et **1264** gènes.
- Réactions communes : **2186**
- Métabolites communs : **1593**
<!-- - Biomasse : 0.982 E.coli et 0.38 Salmonella -->


## **Diapo 38 (facultatif)**

***Combien de moles peut-on en produire par mole de glucose ? Et en concervant une production de biomasse égale à 20% de la production maximale ? Quelles réactions ne peuvent être utilisées que pour produire la molécule d’intérêt et pas pour produire de la biomasse ?***
