import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *


class ObjectCleaning(Module):
    def __init__(self, collectionName, outCollectionName, selection, SFnamePrefix, SFname, SFval):
        self.collectionName = collectionName
        self.outCollectionName = outCollectionName
        self.selection = selection
        self.SFnamePrefix = SFnamePrefix
        self.SFname = SFname
        self.SFval = SFval
        self.doW = ( (SFnamePrefix is not None) or (SFname is not None) or (SFval is not None) )
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.outCollectionName+"_idx", "F", lenVar ="n"+self.outCollectionName);
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

        print 'Length of objs %s: %s'%(self.collectionName,len(objs))

        eventSelW = 1.0
        eventVetoW = 1.0

        cleanObjs_idx = []
        cleanObjs_pt = []
        cleanObjs_eta = []
        cleanObjs_phi = []
        cleanObjs_mass = []

        objIdx = 0
        for obj in objs:
            if not ( eval(self.selection) ):
                #print ' ---- Loop: obj idx %d failed'%objIdx
                objIdx += 1
                continue
            #print ' ---- Loop: obj idx %d passed'%objIdx

            cleanObjs_idx.append(objIdx)
            cleanObjs_pt.append(obj.pt)
            cleanObjs_eta.append(obj.eta)
            cleanObjs_phi.append(obj.phi)
            cleanObjs_mass.append(obj.mass) 

#get scale factors
            if (self.doW):
                #for w in SFweights:
                    #print ' ------ loop weight value: %3.3f'%w.effSF_Loose
                if (self.SFnamePrefix is not None):
                    ret = Object(event,self.collectionName,index=objIdx)
                    #wobj = obj[objIdx].effSF_Loose
                    print ret.__dict__
                    wobj = ret.__dict__[self.SFname]
                else:
                    wobj = SFval

                eventSelW *= wobj
                eventVetoW *= (1-wobj)

            objIdx += 1


        self.out.fillBranch(self.outCollectionName+"_idx", cleanObjs_idx)
        self.out.fillBranch(self.outCollectionName+"_pt", cleanObjs_pt)
        self.out.fillBranch(self.outCollectionName+"_eta", cleanObjs_eta)
        self.out.fillBranch(self.outCollectionName+"_phi", cleanObjs_phi)
        self.out.fillBranch(self.outCollectionName+"_mass", cleanObjs_mass)
        if (self.doW):
            self.out.fillBranch(self.outCollectionName+"_eventSelW",eventSelW)
            self.out.fillBranch(self.outCollectionName+"_eventVetoW",eventVetoW)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

NewJetCleaningConstructor = lambda : ObjectCleaning(collectionName= "Jet", outCollectionName = "CleanJet", selection = 'abs(obj.eta) < 5.0 and ((obj.puId & 0x4) > 0) and ((abs(obj.eta)<=2.7 and ((obj.jetId & 0x4) > 0 )) or (abs(obj.eta) > 2.7 and ((obj.jetId & 0x2) > 0 )))',SFnamePrefix = None, SFname = None, SFval = None)
#TauCleaningConstructor2017 = lambda : ObjectCleaning(collectionName= "tau", outCollectionName = "VLooseTau", 'abs(obj.eta) < 2.3', None, 0.88)
LooseMuonConstructor = lambda : ObjectCleaning(collectionName= "Muon", outCollectionName = "LooseMuon", selection = 'abs(obj.eta) < 2.4 and obj.pt > 10 and obj.pfRelIso04_all < 0.25',SFnamePrefix = 'Muon', SFname = 'effSF_Loose',SFval = None)
