#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from VBFHToInv.NanoAODTools.postprocessing.VBFHToInvModules import *
#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis


p=PostProcessor('.',inputFiles(), modules=[TriggerSelectionConstructor(),JetCleaningConstructor(),puWeight2017(),btagSF2017(),jetmetUncertainties2017All()],provenance=True,fwkJobReport=True)
p.run()

print "DONE"
os.system("ls -lR")

