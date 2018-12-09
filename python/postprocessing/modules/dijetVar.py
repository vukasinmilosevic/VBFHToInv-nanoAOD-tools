import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class DiObjVar(Module):
    def __init__(self, objCollectionName, metCollectionName = "MET"):
        self.objCollectionName = objCollectionName
        self.metCollectionName = metCollectionName
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.metCollectionName+self.objCollectionName+"_MT",  "F");
        self.out.branch("di"+self.objCollectionName+"_M",  "F");
        self.out.branch("di"+self.objCollectionName+"_dEta", "F");
        self.out.branch("di"+self.objCollectionName+"_dPhi", "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        objs = Collection(event, self.objCollectionName)
        
        met_phi = getattr(event, self.metCollectionName+"_phi")
        met_pt = getattr(event, self.metCollectionName+"_pt")
        
        if (len(objs)>=1):
            mt =  2*math.sqrt(met_pt*objs[0].p4().Pt()*(1-math.cos(objs[0].p4().Phi()-met_phi)))
            self.out.fillBranch(self.metCollectionName+self.objCollectionName+"_MT", mt)
        else:
            self.out.fillBranch(self.metCollectionName+self.objCollectionName+"_MT", -1000)
        
        eventSum = ROOT.TLorentzVector()
        if (len(objs)>=2):
            eventSum += (objs[0].p4()+objs[1].p4())
            self.out.fillBranch("di"+self.objCollectionName+"_M", eventSum.M())
            self.out.fillBranch("di"+self.objCollectionName+"_dEta", abs(objs[0].p4().Eta()-objs[1].p4().Eta()))
            self.out.fillBranch("di"+self.objCollectionName+"_dPhi", abs(deltaPhi(objs[0].p4().Phi(), objs[1].p4().Phi())))
        else:
            self.out.fillBranch("di"+self.objCollectionName+"_M", -1000)
            self.out.fillBranch("di"+self.objCollectionName+"_dEta", -1000)
            self.out.fillBranch("di"+self.objCollectionName+"_dPhi", -1000)
        
        
        
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed




DiCleanJetVariableConstructor = lambda : DiObjVar(objCollectionName= "CleanJet")
DiLooseMuonVariableConstructor = lambda : DiObjVar(objCollectionName= "LooseMuon", metCollectionName= "MetNoLooseMuon")
DiElectronVariableConstructor = lambda : DiObjVar(objCollectionName= "Electron", metCollectionName= "MetNoElectron")
 
