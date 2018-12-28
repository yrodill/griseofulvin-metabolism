# coding: utf-8

from cobra import *
import cobra.test
from cobra.flux_analysis import *
import csv

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

modelTextbook = cobra.test.create_test_model("textbook")
prod_env = production_envelope(modelTextbook, reactions = ["EX_o2_e"], objective = "EX_ac_e", carbon_sources = "EX_glc__D_e")
prod_env2 = production_envelope(modelTextbook, ["EX_glc__D_e", "EX_o2_e"])
