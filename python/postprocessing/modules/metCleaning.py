import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class MetCleaning(Module):
    def __init__(self, metCollectionName = "MET", lep1CollectionName = "Muon", lep2CollectionName = "Electron", jetCollectionName = "Jet"):
        self.lep1CollectionName = lep1CollectionName
        self.lep2CollectionName = lep2CollectionName
        self.jetCollectionName = jetCollectionName
        self.metCollectionName = metCollectionName
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MetNo"+self.lep1CollectionName+"_pt", "F");
        self.out.branch("MetNo"+self.lep1CollectionName+"_phi", "F");
        self.out.branch("MetNo"+self.lep1CollectionName+"_"+self.jetCollectionName+"_mindPhi", "F");
        self.out.branch("MetNo"+self.lep2CollectionName+"_pt", "F");
        self.out.branch("MetNo"+self.lep2CollectionName+"_phi", "F");
        self.out.branch("MetNo"+self.lep2CollectionName+"_"+self.jetCollectionName+"_mindPhi", "F");
        self.out.branch("MetNoLep_pt", "F");
        self.out.branch("MetNoLep_phi", "F");
        self.out.branch("MetNoLep_"+self.jetCollectionName+"_mindPhi", "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        leptons1 = Collection(event, self.lep1CollectionName)
        leptons2 = Collection(event, self.lep2CollectionName)
        #print "--MAINT TEST: LEPTON COLL 1 size = ", len(leptons1), "LEPTON COLL 2 size =", len(leptons2) 
        jets_phi = getattr(event, self.jetCollectionName+"_phi")
        
        met_phi = getattr(event, self.metCollectionName+"_phi")
        met_pt = getattr(event, self.metCollectionName+"_pt")
        # filling the branch for Met without leptons type 1 and mindPhi Jet/Met
        #print "--INFO: Calling of Lep1 cleaning"
        cleanMetNoLep1_pt, cleanMetNoLep1_phi = MetCleaningProcedure(met_pt, met_phi, leptons1)
        mindPhilep1_ok, mindPhiLep1 = FormJetMetMinDphi(cleanMetNoLep1_phi, jets_phi, len(jets_phi))
        
        if mindPhilep1_ok:
            self.out.fillBranch("MetNo"+self.lep1CollectionName+"_"+self.jetCollectionName+"_mindPhi", mindPhiLep1)
        else:
            self.out.fillBranch("MetNo"+self.lep1CollectionName+"_"+self.jetCollectionName+"_mindPhi", -1000)
        self.out.fillBranch("MetNo"+self.lep1CollectionName+"_pt", cleanMetNoLep1_pt)
        self.out.fillBranch("MetNo"+self.lep1CollectionName+"_phi", cleanMetNoLep1_phi)
        
        
        # filling the branch for Met without leptons type 2i
        #print "--INFO: Calling of Lep2 cleaning"
        cleanMetNoLep2_pt, cleanMetNoLep2_phi = MetCleaningProcedure(met_pt, met_phi, leptons2)
        mindPhilep2_ok, mindPhiLep2 = FormJetMetMinDphi(cleanMetNoLep2_phi, jets_phi, len(jets_phi))
        
        if mindPhilep2_ok:
            self.out.fillBranch("MetNo"+self.lep2CollectionName+"_"+self.jetCollectionName+"_mindPhi", mindPhiLep2)
        else:
            self.out.fillBranch("MetNo"+self.lep2CollectionName+"_"+self.jetCollectionName+"_mindPhi", -1000)
        
        self.out.fillBranch("MetNo"+self.lep2CollectionName+"_pt", cleanMetNoLep2_pt)
        self.out.fillBranch("MetNo"+self.lep2CollectionName+"_phi", cleanMetNoLep2_phi)
        
        # filling the branch for Met without leptons
        #print "--INFO: Calling of all LEP cleaning"
	cleanMetNoLep_pt, cleanMetNoLep_phi = MetCleaningProcedure(met_pt, met_phi, leptons1, leptons2)
        mindPhilep_ok, mindPhiLep = FormJetMetMinDphi(cleanMetNoLep_phi, jets_phi, len(jets_phi))

        if mindPhilep_ok:
            self.out.fillBranch("MetNoLep_"+self.jetCollectionName+"_mindPhi", mindPhiLep)
        else:
            self.out.fillBranch("MetNoLep_"+self.jetCollectionName+"_mindPhi", -1000)

        self.out.fillBranch("MetNoLep_pt", cleanMetNoLep_pt)
        self.out.fillBranch("MetNoLep_phi", cleanMetNoLep_phi)

        return True

def MetCleaningProcedure(met_pt, met_phi, leptons1, leptons2 = None):
    met_x = met_pt*math.cos(met_phi)
    met_y = met_pt*math.sin(met_phi)
   # print "Length of the first lep collection = ", len(leptons1)
    if len(leptons1)>0:
#	print "Lep coll1 ok"
        for lep in leptons1 :
            met_x+=lep.pt*math.cos(lep.phi)
            met_y+=lep.pt*math.sin(lep.phi)

 #   print "Test if the second lep collection is called", (leptons2!=None)
   
    if leptons2:
#	print "Lepton collection 2 ok, with length of:", len(leptons2)
        if len(leptons2)>0:
            for lep in leptons2 :
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
    return CleanMet, CleanMetPhi

def FormJetMetMinDphi(met_phi, jet_phi, n_jets):
    if (n_jets>0):
        if n_jets>=4:
            indx = 4
        else:
            indx = n_jets
#	print "--Start: met_phi =", met_phi, "jet_phi[0] = ", jet_phi[0], "nJets =", n_jets
        Min = abs(deltaPhi(jet_phi[0], met_phi)) 
#      	print "--Info : mindPhi initialisation: Min =", Min  
        for i  in range(1,indx):
            phi = abs(deltaPhi(jet_phi[i], met_phi))
 #           print "--Info: jet_phi =", jet_phi[i], " dphi =", phi
            if (Min>phi):
                Min = phi
  #       	print "--Info : mindPhi change: Min =", Min
        return True, Min
    else:
        return False, 0.0


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

MetCleaningConstructor_baseLeptons = lambda : MetCleaning(metCollectionName = "MET", lep1CollectionName= "Muon", lep2CollectionName= "Electron")
MetCleaningConstructor_baseLooseLeptons = lambda : MetCleaning(metCollectionName = "MET", lep1CollectionName= "LooseMuon", lep2CollectionName= "VetoElectron", jetCollectionName = "CleanJet")

