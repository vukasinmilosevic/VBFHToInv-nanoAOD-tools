import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class CRDiLepCreator(Module):
    def __init__(self, LooseLepCollectionName = "Muon", TightLepCollectionName = "Muon", LooseLepVetoCollectionName = "Electron", TightLepVetoCollectionName = "Electron", Selection = "DiLep_mass>60 and DiLep_mass<120 and pt1>20 and pt2>10"):
        self.LooseLepCollectionName = LooseLepCollectionName
        self.TightLepCollectionName = TightLepCollectionName
        self.LooseLepVetoCollectionName = LooseLepVetoCollectionName
        self.TightLepVetoCollectionName = TightLepVetoCollectionName
        self.Selection = Selection
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        if "muon" in self.LooseLepCollectionName.lower():
            self.out.branch("CR_DiMuon_mass", "F")
            self.out.branch("CR_Zmumu", "F");
        else:
            self.out.branch("CR_DiElectron_mass", "F")
            self.out.branch("CR_Zee", "F");


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
        
        DiObjMass = -1000
        CR_Zee = 0
        CR_Zmumu = 0
        
        if (nLooseVetoLeptons == 0) and (nTightVetoLeptons == 0) and nTightLeptons>0 and nLooseLeptons>=0 and (nLooseLeptons+nTightLeptons)==2:
            DiLep_mass = -1000
            if nTightLeptons == 1:
                pt1 = TightLeptons[0].p4().Pt()
                pt2 = LooseLeptons[0].p4().Pt()
                if pt2>pt1:
                    temp = pt1
                    pt1 = pt2
                    pt2 = temp
                
                DiLep_mass = (TightLeptons[0].p4()+LooseLeptons[0].p4()).M()
                
            elif nTightLeptons == 2:
                DiLep_mass = (TightLeptons[0].p4()+TightLeptons[1].p4()).M()
                pt1 = TightLeptons[0].p4().Pt()
                pt2 = TightLeptons[1].p4().Pt()
            else:
                print "This should not be happening: NLoose = ", nLooseLeptons, "NTight = ", nTightLeptons
            
            if eval(self.Selection):
                DiObjMass = DiLep_mass
                if "muon" in self.LooseLepCollectionName.lower():
                    CR_Zmumu = 1
                else:
                    CR_Zee = 1
        
        if "muon" in self.LooseLepCollectionName.lower():
            self.out.fillBranch("CR_Zmumu", CR_Zmumu)
            self.out.fillBranch("CR_DiMuon_mass", DiObjMass)
        else:
            self.out.fillBranch("CR_Zee", CR_Zee)
            self.out.fillBranch("CR_DiElectron_mass", DiObjMass)
        
            



        return True
           
                        


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

CRDiMuonCreatorConstructor = lambda : CRDiLepCreator( LooseLepCollectionName = "CRLooseMuon", TightLepCollectionName = "CRTightMuon",  LooseLepVetoCollectionName = "CRVetoElectron", TightLepVetoCollectionName = "CRTightElectron")
CRDiElectronCreatorConstructor = lambda : CRDiLepCreator( LooseLepCollectionName = "CRVetoElectron", TightLepCollectionName = "CRTightElectron", LooseLepVetoCollectionName = "CRLooseMuon", TightLepVetoCollectionName = "CRTightMuon")

