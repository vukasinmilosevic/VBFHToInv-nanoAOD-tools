#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from VBFHToInv.NanoAODTools.postprocessing.VBFHToInvModules import *

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis



p=PostProcessor('.',inputFiles(), modules=[TriggerSelectionConstructor(),JetCleaningConstructor()],provenance=True,fwkJobReport=True,jsonInput='Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt')
p.run()

print "DONE"
os.system("ls -lR")

#modules=[TriggerSelectionConstructor(),JetCleaningConstructor(),LooseMuonConstructor(),CRLooseMuonConstructor(),CRTightMuonConstructor(),LooseElectronConstructor(),CRLooseElectronConstructor(),CRTightElectronConstructor(),VLooseTauConstructor(),LoosePhotonConstructor(),MediumBJetConstructor(),MetCleaningConstructor_baseLooseLeptons(),DiCleanJetVariableConstructor(),CRDiMuonCreatorConstructor(),CRDiElectronCreatorConstructor(),CRSingleMuonCreatorConstructor(),CRSingleElectronCreatorConstructor(),SelectionCreatorConstructor()]
