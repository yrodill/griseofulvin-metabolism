# coding: utf-8
from cobra import *
from cobra.flux_analysis import *
import cobra.test
import os
from os.path import join

#Escherichia coli str. K-12 substr. MG1655
#model on bigg : Model: iJO1366 => http://bigg.ucsd.edu/models/iJO1366
modelEcoli = cobra.test.create_test_model("ecoli")

reacs = []

print("Load JSON object ...")
model = cobra.io.load_json_model("metacyc.json")
print("Loading done.")
# print(model.__dict__)
griseofulvin = model.metabolites.get_by_id("CPD__45__17786_c")
# nadph = model.metabolites.get_by_id("NADPH_c")
# proton = model.metabolites.get_by_id("PROTON_c")

# print(griseofulvin)

createGriseofulvin = model.reactions.get_by_id("RXN__45__16539")

# print(griseofulvin.reactions)

# print("Searching metabolites")
# for i in range(len(model.metabolites)):
#     if(model.metabolites[i].name == "griseofulvin"):
#         metabolites.append(model.metabolites[i])
# print(metabolites[0].reactions)


# print(createGriseofulvin.name)
# print(createGriseofulvin.subsystem)

# for metabo in createGriseofulvin.metabolites:
#     print(metabo.name, ":",metabo.charge)

# # print(createGriseofulvin.metabolites)
# print(createGriseofulvin.upper_bound)

createGriseofulvin.add_metabolites({model.metabolites.get_by_id("NADPH_c"): -1})
createGriseofulvin.add_metabolites({model.metabolites.get_by_id("CPD__45__17786_c"): 1})
createGriseofulvin.add_metabolites({model.metabolites.get_by_id("CPD__45__17793_c"): -1})
createGriseofulvin.add_metabolites({model.metabolites.get_by_id("NADP_c"): 1})
createGriseofulvin.add_metabolites({model.metabolites.get_by_id("PROTON_c"): -1})

for reaction in model.reactions:
    if(reaction.subsystem == "PWY-7653"):
        # print(reaction.metabolites)
        reacs.append(reaction)

for i in range(len(reacs)):
        for metabo in reacs[i].metabolites:
                metabo.id = metabo.id.lower()
                print "Metabolites id : ",metabo.id
                print "Value : ",reacs[i].metabolites[metabo]

# for reac in modelEcoli.boundary:
#     print(reac)

# modelEcoli.add_reactions(griseofulvin.reactions)
# modelEcoli.add_reactions(nadph.reactions)
# modelEcoli.add_reactions(proton.reactions)
# modelEcoli.add_boundary(griseofulvin,type="exchange",ub=1000.0)
modelEcoli.add_reactions(reacs)
print('Ce modèle contient %i réactions'% len(modelEcoli.reactions))
print('Ce modèle contient %i métabolites'% len(modelEcoli.metabolites))

modelEcoli.objective = "RXN__45__16539"
solution = modelEcoli.optimize()
fluxMax = solution.objective_value
print(fluxMax)


modelEcoli.summary()

