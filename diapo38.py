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
        if(reaction.subsystem == "PWY-7653"):
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

modelEcoli.objective = "RXN__45__16539"
solution = modelEcoli.optimize()
fluxMax = solution.objective_value
print(fluxMax)

modelEcoli.summary()
# modelEcoli.summary(fva=0.95)

print "Writing JSON model for comparison ...\n"
cobra.io.save_json_model(modelEcoli, "./test.json")
print "Done!\n"

print model.metabolites.CPD__45__17786_c.summary()
# print model.metabolites.h_c.summary()
# print model.metabolites.nadph_c.summary()

