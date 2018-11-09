#Import all the modules defined in /modules
import os

#adding specific VBF variables to the trees
from VBFHToInv.NanoAODTools.postprocessing.modules.dijetVar import DiJetVariableConstructor
from VBFHToInv.NanoAODTools.postprocessing.modules.jetMetmindphi import JetMetMinDPhiConstructor
from VBFHToInv.NanoAODTools.postprocessing.modules.MetCleaning import MetCleaningConstructor
from VBFHToInv.NanoAODTools.postprocessing.modules.lepSFProducer import lepSFtight
from VBFHToInv.NanoAODTools.postprocessing.modules.lepSFProducer import lepSFveto
from VBFHToInv.NanoAODTools.postprocessing.modules.jetCleaning import JetCleaningConstructor
from VBFHToInv.NanoAODTools.postprocessing.modules.trigger_selection import TriggerSelectionConstructor

#btagging weights - give event weight automatically based on jets discri (so all working points automatically)
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSF2017


#pu weight - data file is hardcoded !!!
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeightProducer
pufile_data="%s/src/VBFHToInv/NanoAODTools/data/pileup/RerecoData2017withSysts.root" % os.environ['CMSSW_BASE']
puWeight2017 = lambda : puWeightProducer('auto',pufile_data,"pu_mc","pileup",verbose=False)

#how to change data and MC files ??
#pufile_data2017="%s/src/VBFHToInv/NanoAODTools/python/postprocessing/data/pileup/pileup_Cert_294927-306462_13TeV_PromptReco_Collisions17_withVar.root" % os.environ['CMSSW_BASE']
#pufile_mcFall17="%s/src/VBFHToInv/NanoAODTools/python/postprocessing/data/pileup/" % os.environ['CMSSW_BASE']
#puWeight2017 = lambda : puWeightProducer(pufile_mcFall17,pufile_data2017,"pu_mc","pileup",verbose=False)

#lepton SF
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import lepSF

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2017All
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2017

