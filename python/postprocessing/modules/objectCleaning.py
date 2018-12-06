import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *


class ObjectCleaning(Module):
    def __init__(self, collectionName, outCollectionName, selection, SFname, SFval):
        self.collectionName = collectionName
        self.outCollectionName = outCollectionName
        self.selection = selection
        self.SFname = SFname
        self.SFval = SFval
        self.eventSelW = 1.0
        self.eventVetoW = 1.0
        self.doW = ( (SFname is not None) or (SFval is not None) )
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.outCollectionName+"_pt", "F", lenVar ="n"+self.outCollectionName);
        self.out.branch(self.outCollectionName+"_eta", "F", lenVar ="n"+self.outCollectionName);
        self.out.branch(self.outCollectionName+"_phi", "F", lenVar ="n"+self.outCollectionName);
        self.out.branch(self.outCollectionName+"_mass", "F", lenVar ="n"+self.outCollectionName);
        if (self.doW):
            self.out.branch(self.outCollectionName+"_eventSelW", "F");
            self.out.branch(self.outCollectionName+"_eventVetoW", "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        objs = Collection(event, self.collectionName)
        if (self.doW):
            if (self.SFname is not None): SFweights = Collection(event, self.SFname,"n"+self.collectionName)
            else: 
                SFweights = [SFval] * len(objs)
                
            print SFweights
            self.eventSelW = 1.0
            self.eventVetoW = 1.0
            
        cleanObjs_pt = []
        cleanObjs_eta = []
        cleanObjs_phi = []
        cleanObjs_mass = []

        objIdx = 0
        for obj in objs:
            if not (self.selection):
                objIdx += 1
                continue

            cleanObjs_pt.append(obj.pt)
            cleanObjs_eta.append(obj.eta)
            cleanObjs_phi.append(obj.phi)
            cleanObjs_mass.append(obj.mass) 

#get scale factors
            if (self.doW):
                self.eventSelW *= SFweights[objIdx]
                self.eventVetoW *= (1-SFweights[objIdx])

            objIdx += 1


        self.out.fillBranch(self.outCollectionName+"_pt", cleanObjs_pt)
        self.out.fillBranch(self.outCollectionName+"_eta", cleanObjs_eta)
        self.out.fillBranch(self.outCollectionName+"_phi", cleanObjs_phi)
        self.out.fillBranch(self.outCollectionName+"_mass", cleanObjs_mass)
        if (self.doW):
            self.out.fillBranch(self.outCollectionName+"_eventSelW",self.eventSelW)
            self.out.fillBranch(self.outCollectionName+"_eventVetoW",self.eventVetoW)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

NewJetCleaningConstructor = lambda : ObjectCleaning(collectionName= "Jet", outCollectionName = "CleanJet", selection = 'abs(obj.eta) < 5.0 and ((obj.puId & 0x4) > 0) and ((abs(obj.eta)<=2.7 and ((obj.jetId & 0x4) > 0 )) or (abs(obj.eta) > 2.7 and ((obj.jetId & 0x2) > 0 )))',SFname = None, SFval = None)
#TauCleaningConstructor2017 = lambda : ObjectCleaning(collectionName= "tau", outCollectionName = "VLooseTau", 'abs(obj.eta) < 2.3', None, 0.88)
LooseMuonConstructor = lambda : ObjectCleaning(collectionName= "Muon", outCollectionName = "LooseMuon", selection = 'abs(obj.eta) < 2.4 and obj.pt > 10 and obj.pfRelIso04_all < 0.25',SFname = 'Muon_effSF_Loose',SFval = None)
