import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class DiJetVar(Module):
    def __init__(self, jetCollectionName):
        self.jetCollectionName = jetCollectionName
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("leading_Mjj",  "F");
	self.out.branch("leading_dEtajj", "F");
        self.out.branch("leading_dPhijj", "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, self.jetCollectionName)
        
        eventSum = ROOT.TLorentzVector()
        if (len(jets)>=2):
           eventSum += (jets[0].p4()+jets[1].p4())
           self.out.fillBranch("leading_Mjj",eventSum.M())
           self.out.fillBranch("leading_dPhijj", deltaPhi(jets[0].p4().Phi(), jets[1].p4().Phi()))
           self.out.fillBranch("leading_dEtajj", abs(jets[0].p4().Eta()-jets[1].p4().Eta()))
        else:
	   self.out.fillBranch("leading_Mjj",-1000)
           self.out.fillBranch("leading_dPhijj", -1000)
           self.out.fillBranch("leading_dEtajj", -1000)
        return True

def DiJetVariables(jets_pt, jets_eta, jets_phi, jets_m):
    eventSum = ROOT.TLorentzVector()
    jet1 = ROOT.TLorentzVector()
    jet2 = ROOT.TLorentzVector()
    if (len(jets_pt)>=2):
        jet1.SetPtEtaPhiM(jets_pt[0],jets_eta[0],jets_phi[0],jets_m[0])
        jet2.SetPtEtaPhiM(jets_pt[1],jets_eta[1],jets_phi[1],jets_m[1])
        eventSum += (jet1+jet2)
        leading_Mjj = eventSum.M()
        leading_dPhijj = deltaPhi(jets_phi[0], jets_phi[1])
        leading_dEtajj =  abs(jets_eta[0]-jets_eta[1])
        return True, leading_Mjj, leading_dPhijj, leading_dEtajj
    else:
        return False, 0.0, 0.0, 0.0
	

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed




DiJetVariableConstructor = lambda : DiJetVar(jetCollectionName= "Jet") 
 
