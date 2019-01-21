import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class CRCreator(Module):
    def __init__(self, metCollectionName = "MET", LooseLep1CollectionName = "Muon", TightLep1CollectionName = "Muon", LooseLep2CollectionName = "Electron", TightLep2CollectionName = "Electron"):
        self.metCollectionName = metCollectionName
        self.LooseLep1CollectionName = LooseLep1CollectionName
        self.TightLep1CollectionName = TightLep1CollectionName
        self.LooseLep2CollectionName = LooseLep2CollectionName
        self.TightLep2CollectionName = TightLep2CollectionName
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("CR_Flag", "I");
        self.out.branch("CR_DiMuon_mass", "F");
        self.out.branch("CR_Muon_MT", "F");
        #self.out.branch("CR_DiElectron_mass", "F");
        #self.out.branch("CR_Electron_MT", "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        LooseLeptons1 = Collection(event, self.LooseLep1CollectionName)
        TightLeptons1 = Collection(event, self.TightLep1CollectionName)
        
        nLooseLeptons1 = getattr(event, "n"+self.LooseLep1CollectionName)
        nTightLeptons1 = getattr(event, "n"+self.TightLep1CollectionName)
        
        LooseLeptons2 = Collection(event, self.LooseLep2CollectionName)
        TightLeptons2 = Collection(event, self.TightLep2CollectionName)
            
        nLooseLeptons2 = getattr(event, "n"+self.LooseLep2CollectionName)
        nTightLeptons2 = getattr(event, "n"+self.TightLep2CollectionName)
        
        met_phi = getattr(event, self.metCollectionName+"_phi")
        met_pt = getattr(event, self.metCollectionName+"_pt")
        
        # Single Muon CR check
        if nLooseLeptons2 == 0:
            if nTightLeptons1 == 1 and nLooseLeptons1 ==0:
                mt =  2*math.sqrt(met_pt*TightLeptons1[0].p4().Pt()*(1-math.cos(TightLeptons1[0].p4().Phi()-met_phi)))
                self.out.fillBranch("CR_Flag", 1)
                self.out.fillBranch("CR_Muon_MT", mt)
                self.out.fillBranch("CR_DiMuon_mass", -1000)
                
		return True
        #Double Muon CR check
            elif nTightLeptons1>0 and nLooseLeptons1>=0 and (nLooseLeptons1+nTightLeptons1)==2:
                if nTightLeptons1 == 1:
                    pt1 = TightLeptons1[0].p4().Pt()
                    pt2 = LooseLeptons1[0].p4().Pt()
		    if pt2>pt1:
		    	temp = pt1
			pt1 = pt2
			pt2 = temp
                
		    DiMuon_mass = (TightLeptons1[0].p4()+LooseLeptons1[0].p4()).M()
                
		elif nTightLeptons1 == 2:
                    DiMuon_mass = (TightLeptons1[0].p4()+TightLeptons1[1].p4()).M()
                    pt1 = TightLeptons1[0].p4().Pt()
                    pt2 = TightLeptons1[1].p4().Pt()
                else:
                    print "This should not be happening: NLoose = ", nLooseLeptons1, "NTight = ", nTightLeptons1
        
                if DiMuon_mass>60 and DiMuon_mass<120 and pt1>20 and pt2>10:
                    self.out.fillBranch("CR_Flag", 2)
                    self.out.fillBranch("CR_DiMuon_mass", DiMuon_mass)
                    self.out.fillBranch("CR_Muon_MT", -1000)
		    return True
                else:
                    #self.out.fillBranch("CR_Flag", -2)
                    #self.out.fillBranch("CR_DiMuon_mass", -1000)
                    #self.out.fillBranch("CR_Muon_MT", -1000)
                    return False
                        
        #If None of the above CR_Flag == 0
            else:
                #self.out.fillBranch("CR_Flag", 0)
                #self.out.fillBranch("CR_Muon_MT", -1000)
                #self.out.fillBranch("CR_DiMuon_mass", -1000)
        #If only looking in the CRs
                return False
        else:
		#return False 
                return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

CRCreatorConstructor = lambda : CRCreator(metCollectionName = "MetNoLooseMuon", LooseLep1CollectionName = "CRLooseMuon", TightLep1CollectionName = "CRTightMuon", LooseLep2CollectionName = "Electron", TightLep2CollectionName = "Electron")


