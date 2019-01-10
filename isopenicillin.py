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

for reaction in model.reactions:
        if(reaction.subsystem == "PWY-5629, PWY-5634"):
                reacs.append(reaction)

metabo_list = []
for i in range(len(reacs)):
        for metabo in reacs[i].metabolites:
                print metabo.name
                a=0
                for metabolite in modelEcoli.metabolites:
                        if metabolite.formula == metabo.formula and a == 0:
                                print "ID from ecoli model : ",metabolite.id
                                a += 1
                                print "Metabolites id : ",metabo.id
                                metabo.id = metabolite.id
                        if metabo not in metabo_list and metabo not in modelEcoli.metabolites:
                                metabo_list.append(metabo)
                                
                print "Metabolites change id : ",metabo.id
                print "Value : ",reacs[i].metabolites[metabo]
                print "\n"

print metabo_list

print('Ce modèle contient %i réactions'% len(modelEcoli.reactions))
print('Ce modèle contient %i métabolites'% len(modelEcoli.metabolites))
print "Adding reactions and metabolites...\nDone\n"
modelEcoli.add_metabolites(metabo_list)
modelEcoli.add_reactions(reacs)
print('Ce modèle contient %i réactions'% len(modelEcoli.reactions))
print('Ce modèle contient %i métabolites'% len(modelEcoli.metabolites))

modelEcoli.summary()

ISOPENICILLIN__45__N_c = modelEcoli.metabolites.get_by_id("ISOPENICILLIN__45__N_c")

reactionExp_isopenicillin = Reaction(
        id = "export_isopenicillin",
        name = "reaction export isopenicillin (objective reaction)",
        lower_bound = 0,
        upper_bound = 1000
)
reactionExp_isopenicillin.add_metabolites({ISOPENICILLIN__45__N_c:-1})

modelEcoli.add_reactions([reactionExp_isopenicillin])

# print "Writing JSON model for comparison ...\n"
# cobra.io.save_json_model(modelEcoli, "./test.json")
# print "Done!\n"

# medium["CPD__45__17786_c"]=1000.0

index=0
for i in range(len(modelEcoli.metabolites)):
        if(modelEcoli.metabolites[i].id == "N__45__5S__45__5__45__AMINO__45__5__45__CARBOXYPENTANOYL__45__L__45__CY_c"):
                index=i
                print(index)

modelEcoli.add_boundary(modelEcoli.metabolites[index], type="exchange", reaction_id="RX__45__16539",lb=None, ub=1000.0)

modelEcoli.objective = "export_isopenicillin"
solution = modelEcoli.optimize()
fluxMax = solution.objective_value
print(fluxMax)

modelEcoli.summary()
# modelEcoli.summary(fva=0.95)
