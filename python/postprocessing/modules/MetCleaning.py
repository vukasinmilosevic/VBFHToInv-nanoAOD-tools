import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MetCleaning(Module):
    def __init__(self, lepCollectionName, metCollectionName):
        self.lepCollectionName = lepCollectionName
        self.metCollectionName = metCollectionName
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MetNo"+self.lepCollectionName+"_pt", "F");
        self.out.branch("MetNo"+self.lepCollectionName+"_phi", "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        leptons = Collection(event, self.lepCollectionName)
        met_phi = getattr(event, self.metCollectionName+"_phi")
        met_pt = getattr(event, self.metCollectionName+"_pt")
        
        met_x = met_pt*math.cos(met_phi)
        met_y = met_pt*math.sin(met_phi)
        if (len(leptons)>0):
           for lep in leptons:
              met_x+=lep.p4().Pt()*math.cos(lep.p4().Phi())
              met_y+=lep.p4().Pt()*math.sin(lep.p4().Phi())

        CleanMet = math.sqrt(met_x**2+met_y**2)
        self.out.fillBranch("MetNo"+self.lepCollectionName+"_pt", CleanMet)
        self.out.fillBranch("MetNo"+self.lepCollectionName+"_phi", math.atan(1.0*met_y/met_x))
        return True

def MetCleaningProcedure(met_pt, met_phi, leptons):
    met_x = met_pt*math.cos(met_phi)
    met_y = met_pt*math.sin(met_phi)
    if len(leptons)>0:
           for lep in leptons :
              met_x+=lep.pt*math.cos(lep.phi)
              met_y+=lep.pt*math.sin(lep.phi)

    CleanMet = math.sqrt(met_x**2+met_y**2)
    CleanMetPhi = math.acos(met_x/CleanMet)
    if met_x < 0:
        if  met_y < 0 :
	    CleanMetPhi*=-1.
    else:
        if  met_y < 0 :
            CleanMetPhi*=-1.

    return True, CleanMet, CleanMetPhi

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

MetCleaningConstructor = lambda : MetCleaning(lepCollectionName= "Muon", metCollectionName = 'MET') 
 
