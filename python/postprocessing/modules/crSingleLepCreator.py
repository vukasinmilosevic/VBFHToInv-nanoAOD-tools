import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class CRSingleLepCreator(Module):
    def __init__(self, metCollectionName = "MET", LooseLepCollectionName = "Muon", TightLepCollectionName = "Muon", LooseLepVetoCollectionName = "Electron", TightLepVetoCollectionName = "Electron"):
        self.metCollectionName = metCollectionName
        self.LooseLepCollectionName = LooseLepCollectionName
        self.TightLepCollectionName = TightLepCollectionName
        self.LooseLepVetoCollectionName = LooseLepVetoCollectionName
        self.TightLepVetoCollectionName = TightLepVetoCollectionName
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("CR_Flag", "F");
        if "muon" in self.LooseLepCollectionName.lower():
            self.out.branch("CR_Muon_MT", "F")
        else:
            self.out.branch("CR_Electron_MT", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        LooseLeptons = Collection(event, self.LooseLepCollectionName)
        TightLeptons = Collection(event, self.TightLepCollectionName)
        
        nLooseLeptons = getattr(event, "n"+self.LooseLepCollectionName)
        nTightLeptons = getattr(event, "n"+self.TightLepCollectionName)
        
        nLooseVetoLeptons = getattr(event, "n"+self.LooseLepVetoCollectionName)
        nTightVetoLeptons = getattr(event, "n"+self.TightLepVetoCollectionName)
        
        met_phi = getattr(event, self.metCollectionName+"_phi")
        met_pt = getattr(event, self.metCollectionName+"_pt")
        
        # Single Muon CR check
        if (nLooseVetoLeptons == 0) and (nTightVetoLeptons == 0):
            if nTightLeptons == 1 and nLooseLeptons ==0:
                mt =  2*math.sqrt(met_pt*TightLeptons[0].p4().Pt()*(1-math.cos(TightLeptons[0].p4().Phi()-met_phi)))
                if "muon" in self.LooseLepCollectionName.lower():
                    self.out.fillBranch("CR_Flag", 1)
                    self.out.fillBranch("CR_Muon_MT", mt)
                else:
                    self.out.fillBranch("CR_Flag", 3)
                    self.out.fillBranch("CR_Electron_MT", mt)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

CRSingleMuonCreatorConstructor = lambda : CRSingleLepCreator(metCollectionName = "MetNoLooseMuon", LooseLepCollectionName = "CRLooseMuon", TightLepCollectionName = "CRTightMuon", LooseLepVetoCollectionName = "CRVetoElectron", TightLepVetoCollectionName = "CRTightElectron")
CRSingleElectronCreatorConstructor = lambda : CRSingleLepCreator(metCollectionName = "MetNoVetoElectron", LooseLepCollectionName = "CRVetoElectron", TightLepCollectionName = "CRTightElectron", LooseLepVetoCollectionName = "CRLooseMuon", TightLepVetoCollectionName = "CRTightMuon")


