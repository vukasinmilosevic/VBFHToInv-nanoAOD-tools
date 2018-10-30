#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from VBFHToInv.NanoAODTools.postprocessing.VBFHToInvModules import *
from VBFHToInv.NanoAODTools.postprocessing.modules.HLT_Paths import *
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

p=PostProcessor('.',inputFiles(), selection, modules=[JetCleaningConstructor(),puWeight2017(),btagSF2017(),jetmetUncertainties2017All()],provenance=True,fwkJobReport=True)
p.run()

print "DONE"
os.system("ls -lR")

