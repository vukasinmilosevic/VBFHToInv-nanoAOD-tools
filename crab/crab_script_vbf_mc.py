#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from VBFHToInv.NanoAODTools.postprocessing.VBFHToInvModules import *
#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis


p=PostProcessor('.',inputFiles(), modules=[TriggerSelectionConstructor(),JetCleaningConstructor(),puWeight2017(),btagSF2017(),lepSFtight(),lepSFveto(),jetmetUncertainties2017(),jecUncert_2017_MC()],provenance=True,fwkJobReport=True)
p.run()

print "DONE"
os.system("ls -lR")

