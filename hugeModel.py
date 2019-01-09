# coding: utf-8
from cobra import *
import pandas as pd
import cobra.test

modelEcoli=cobra.test.create_test_model("ecoli")
modelSalmonella=cobra.test.create_test_model("salmonella")

# ----------------
#       E.coli
# ----------------
print("# E.coli\n")
print('Ce modèle contient %i réactions'% len(modelEcoli.reactions))
print('Ce modèle contient %i métabolites'% len(modelEcoli.metabolites))
print('Ce modèle contient %i genes'% len(modelEcoli.genes))

# for reac in modelEcoli.boundary:
#     print(reac)

# __________ Modif
solution = modelEcoli.optimize()
fluxMax = solution.objective_value
print("\n")
print(fluxMax)

modelEcoli.summary(fva=0.95)

# flux contenus dans solutions.fluxes
# for reac in modelEcoli.reactions:
# 	print(str(reac.id) + " : " + str(solution.fluxes[reac.id]))


print("\n# End Coli \n\n")
# ----------------
#       Salmonella
# ----------------
print("# Salmonella\n")
print('Ce modèle contient %i réactions'% len(modelSalmonella.reactions))
print('Ce modèle contient %i métabolites'% len(modelSalmonella.metabolites))
print('Ce modèle contient %i genes'% len(modelSalmonella.genes))

# for reac in modelSalmonella.boundary:
#     print(reac)

# __________ Modif
solution = modelSalmonella.optimize()
fluxMax = solution.objective_value
print("\n")
print(fluxMax)

modelSalmonella.summary(fva=0.95)

# flux contenus dans solutions.fluxes
# for reac in modelSalmonella.reactions:
#         print(str(reac.id) + " : " + str(solution.fluxes[reac.id]))

print("\n# End Salmonella")

print("\n# Compute")

cptReac = 0
cptMetabo = 0
for reac in modelEcoli.reactions:
    if reac in modelSalmonella.reactions:
        cptReac +=1

for metabo in modelEcoli.metabolites:
    if metabo in modelSalmonella.metabolites:
        cptMetabo += 1

print('Reactions communes : %i'% cptReac)
print('Metabo communs : %i'% cptMetabo)

# Compare biomass compo
modelEcoli.reactions.get_by_id("Ec_biomass_iJO1366_core_53p95M")
modelSalmonella.reactions.get_by_id("biomass_iRR1083_metals")

# file = open('reaction.txt',"w") 
# file.write(str(modelEcoli.reactions.get_by_id("Ec_biomass_iJO1366_core_53p95M")))
# file.write("\n")
#Ec_biomass_iJO1366_core_53p95M
# file.write(str(modelSalmonella.reactions.get_by_id("biomass_iRR1083_metals")))
# biomass_iRR1083_metals
# print('\nSave done ')
# file.close()


# FVA analyze flux
fvaColi_df = flux_analysis.variability.flux_variability_analysis(modelEcoli, modelEcoli.reactions[:20], fraction_of_optimum = 0.9)
fvaSalmo_df = flux_analysis.variability.flux_variability_analysis(modelSalmonella, modelSalmonella.reactions[:20], fraction_of_optimum = 0.9)
print(fvaColi_df)
print(fvaSalmo_df)
