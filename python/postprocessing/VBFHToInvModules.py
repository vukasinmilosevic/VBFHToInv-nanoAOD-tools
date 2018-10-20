#Import all the modules defined in /modules

#adding specific VBF variables to the trees
from VBFHToInv.NanoAODTools.postprocessing.modules.dijetVar import DiJetVariableConstructor
from VBFHToInv.NanoAODTools.postprocessing.modules.jetMetmindphi import JetMetMinDPhiConstructor
from VBFHToInv.NanoAODTools.postprocessing.modules.MetCleaning import MetCleaningConstructor


#btagging weights - give event weight automatically based on jets discri (so all working points automatically)
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSF2017


#pu weight - data file is hardcoded !!!
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puAutoWeight
#how to change data and MC files ??
#pufile_data2017="%s/src/VBFHToInv/NanoAODTools/python/postprocessing/data/pileup/pileup_Cert_294927-306462_13TeV_PromptReco_Collisions17_withVar.root" % os.environ['CMSSW_BASE']
#pufile_mcFall17="%s/src/VBFHToInv/NanoAODTools/python/postprocessing/data/pileup/" % os.environ['CMSSW_BASE']
#puWeight2017 = lambda : puWeightProducer(pufile_mcFall17,pufile_data2017,"pu_mc","pileup",verbose=False)

#lepton SF
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import lepSF
