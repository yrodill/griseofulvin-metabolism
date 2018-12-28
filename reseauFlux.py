# coding: utf-8

from cobra import *

A = Metabolite(
        id = 'A',
        name = 'metabolite A',
	compartment="coucou")

B = Metabolite(
        id = 'B',
        name = 'metabolite B',
	compartment="coucou")

C = Metabolite(
        id = 'C',
        name = 'metabolite C',
	compartment="coucou")

D = Metabolite(
        id = 'D',
        name = 'metabolite D',
	compartment="coucou")

E = Metabolite(
        id = 'E',
        name = 'metabolite E',
	compartment="coucou")

F = Metabolite(
        id = 'F',
        name = 'metabolite F',
	compartment="coucou")

Biomass = Metabolite(
        id = 'Biomass',
        name = 'metabolite Biomass',
	compartment="coucou")


reaction1 = Reaction(
	id = "R1", 
	name = "reaction 1",
	lower_bound = 0,
	upper_bound = 1000
)
reaction1.add_metabolites({
	A: -1,
        B: -2,
	C: 4
})

reaction2 = Reaction(
	id = "R2", 
	name = "reaction 2",
	lower_bound = 0,
	upper_bound = 1000
)
reaction2.add_metabolites({
        A: -2,
        D: -1,
        E: -1,
	F: 2
})

reaction3 = Reaction(
	id = "R3", 
	name = "reaction 3",
	lower_bound = 0,
	upper_bound = 1000
)
reaction3.add_metabolites({
        F: -1,
	C: 1
})

reaction4 = Reaction(
	id = "R4", 
	name = "reaction 4",
	lower_bound = 0,
	upper_bound = 1000
)
reaction4.add_metabolites({
        B: -1,
	D: 1,
	E: 1
})

reacBiomass = Reaction(
	id = "Rbiomass", 
	name = "reaction biomass",
	lower_bound = 0,
	upper_bound = 1000
)
reacBiomass.add_metabolites({
	C: -2,
	Biomass: 1
})

reacExportBiomass = Reaction(
	id = "Rexp_biomass", 
	name = "reaction export Biomass",
	lower_bound = 0,
	upper_bound = 1000
)
reacExportBiomass.add_metabolites({
	Biomass: -1
})
reacImportB = Reaction(
	id = "RimportB",
	name= "Réaction import B",
	lower_bound = 0,
	upper_bound = 10
)
reacImportB.add_metabolites({
	B : 1
})
reacImportA = Reaction(
	id = "RimportA",
	name= "Réaction import A",
	lower_bound = 0,
	upper_bound = 10
)
reacImportA.add_metabolites({
	A : 1
})


##### Main 
model = Model("Flux")
model.add_reactions([reaction1,reaction2,reaction4,reaction3,reacBiomass,reacImportA,reacImportB,reacExportBiomass])
print('Ce modèle contient %i réactions'% len(model.reactions))
print('Ce modèle contient %i métabolites'% len(model.metabolites))

for reac in model.boundary:
    print(reac)

# __________ Modif
model.objective = "Rbiomass"
solution = model.optimize()
fluxMax = solution.objective_value
print("\n")
print(fluxMax)

model.summary()

solution = model.optimize()
# flux contenus dans solutions.fluxes
for reac in model.reactions:
	print(str(reac.id) + " : " + str(solution.fluxes[reac.id]))

# FVA analyze flux
FVA_result = flux_analysis.variability.flux_variability_analysis(model, fraction_of_optimum = 1.0)

print("\n")
print(FVA_result)
