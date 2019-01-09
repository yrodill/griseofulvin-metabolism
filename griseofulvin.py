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
                print(reaction.check_mass_balance())

#modification des ID (bigg != metacyc)
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

for r in reacs:
        print(r.reaction)

modelEcoli.add_reactions(reacs)
print('Ce modèle contient %i réactions'% len(modelEcoli.reactions))
print('Ce modèle contient %i métabolites'% len(modelEcoli.metabolites))

modelEcoli.summary()

# modelEcoli.objective = "RXN__45__16539"
# solution = modelEcoli.optimize()
# fluxMax = solution.objective_value
# print(fluxMax)

# modelEcoli.summary()


print "Writing JSON model for comparison ...\n"
cobra.io.save_json_model(modelEcoli, "./test.json")
print "Done!\n"

# medium["CPD__45__17786_c"]=1000.0

index=0
for i in range(len(modelEcoli.metabolites)):
        if(modelEcoli.metabolites[i].id == "CPD__45__17793_c"):
                index=i
                print(index)

modelEcoli.add_boundary(modelEcoli.metabolites[index], type="exchange", reaction_id="RX__45__16539",lb=None, ub=1000)

print(modelEcoli.boundary[0:10])
medium = modelEcoli.medium
print modelEcoli.medium
# print model.metabolites.h_c.summary()
# print model.metabolites.nadph_c.summary()

# modelEcoli.summary(fva=0.95)


#reaction de depart : 
#ACP_c + accoa_c + 6.0 h_c + 6.0 malcoa_c --> CPD__45__17794_c + 6.0 co2_c + 7.0 coa_c + h2o_c

ACP_c = modelEcoli.metabolites.get_by_id("ACP_c")
accoa_c = modelEcoli.metabolites.get_by_id("accoa_c")
h_c = modelEcoli.metabolites.get_by_id("h_c")
malcoa_c = modelEcoli.metabolites.get_by_id("malcoa_c")
CPD__45__17786_c = modelEcoli.metabolites.get_by_id("CPD__45__17786_c")



reactionUptake = Reaction(
        id = "uptake",
        name = "reaction uptake",
        lower_bound = 0,
        upper_bound = 1000
)
reactionUptake.add_metabolites({ACP_c:1,accoa_c:1,h_c:6,malcoa_c:6})

reactionExp_griseofulvin = Reaction(
        id = "export_griseofulvin",
        name = "reaction export griseofulvin (objective reaction)",
        lower_bound = 0,
        upper_bound = 1000
)
reactionExp_griseofulvin.add_metabolites({CPD__45__17786_c:-1})

modelEcoli.add_reactions([reactionUptake,reactionExp_griseofulvin])

modelEcoli.objective = "export_griseofulvin"
solution = modelEcoli.optimize()
fluxMax = solution.objective_value
print(fluxMax)


modelEcoli.summary()