#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from VBFHToInv.NanoAODTools.postprocessing.VBFHToInvModules import *
#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor('.',inputFiles(), modules=[nloSF(),bosonDecay(),TriggerSelectionConstructor(),JetCleaningConstructor(),puWeight2017(),btagSF2017deepCSV(),lepSFtight(),lepSFveto(),LooseMuonConstructor(),CRLooseMuonConstructor(),CRTightMuonConstructor(),LooseElectronConstructor(),CRLooseElectronConstructor(),CRTightElectronConstructor(),VLooseTauConstructor(),LoosePhotonConstructor(),MediumBJetConstructor(),MetCleaningConstructor_baseLooseLeptons(),DiCleanJetVariableConstructor(),jetmetUncertainties2017(),jecUncert_2017_MC(),CRDiMuonCreatorConstructor(),CRDiElectronCreatorConstructor(),CRSingleMuonCreatorConstructor(),CRSingleElectronCreatorConstructor(),SelectionCreatorConstructor()],provenance=True,fwkJobReport=True)

p=PostProcessor('.',inputFiles(), modules=[nloSF(),bosonDecay(),lepSFtight(),lepSFveto(),TriggerSelectionConstructor(),LooseMuonConstructor(),LooseElectronConstructor(),JetCleaningConstructorXCl(),puWeight2017(),btagSF2017deepCSV(),CRLooseMuonConstructor(),CRTightMuonConstructor(),CRLooseElectronConstructor(),CRTightElectronConstructor(),VLooseTauConstructor(),LoosePhotonConstructor(),MediumBJetConstructor(),MetCleaningConstructor_baseLooseLeptons(),DiCleanJetVariableConstructor(),jetmetUncertainties2017(),jecUncert_2017_MC(),CRDiMuonCreatorConstructor(),CRDiElectronCreatorConstructor(),CRSingleMuonCreatorConstructor(),CRSingleElectronCreatorConstructor(),SelectionCreatorConstructorTemp()],provenance=True,fwkJobReport=True)


p.run()

print "DONE"
os.system("ls -lR")

