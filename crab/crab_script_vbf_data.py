#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from VBFHToInv.NanoAODTools.postprocessing.VBFHToInvModules import *
from VBFHToInv.NanoAODTools.postprocessing.modules.HLT_Paths_data import *

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis


selection = ""
for hlt in MET_MHT:
    selection+=hlt
    selection+="||"

for hlt in VBF:
    selection+=hlt
    selection+="||"

for hlt in HT:
    selection+=hlt
    selection+="||"

for hlt in HT_MET_MHT:
    selection+=hlt
    selection+="||"

for hlt in Single_Muon:
    selection+=hlt

print selection


p=PostProcessor('.',inputFiles(), selection, modules=[JetCleaningConstructor()],provenance=True,fwkJobReport=True,jsonInput='Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt')
p.run()

print "DONE"
os.system("ls -lR")

