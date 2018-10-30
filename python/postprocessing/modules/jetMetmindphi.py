import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class JetMetMinDPhi(Module):
    def __init__(self, jetCollectionName, metCollectionName):
        self.jetCollectionName = jetCollectionName
        self.metCollectionName = metCollectionName
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("JetMetMin_dPhijj", "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, self.jetCollectionName)
        met_phi = getattr(event, self.metCollectionName+"_phi")
        
        if (len(jets)>0 and met_phi):
           
           Min = 1000000
           for jet in jets:
               phi = abs(jet.p4().Phi()-met_phi)

               if (Min>phi):
			Min = phi
           
           if (Min==1000000):
	       Min = -1000    
           self.out.fillBranch("JetMetMin_dPhijj",Min)
        else:
           self.out.fillBranch("JetMetMin_dPhijj", -1000)
        return True

def FormJetMetMinDphi(met_phi, jet_phi, n_jets):
    if (n_jets>0 and met_phi):
        Min = 1000000
        if n_jets>=4:
            indx = 4
        else:
            indx = n_jets
        
        for i  in range(0,indx):
            phi = abs(jet_phi[i]-met_phi)    
            if (Min>phi):
                Min = phi

        if (Min==1000000):
           return False, 0.0
        else:
           return True, Min
    else:
        return False, 0.0



# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

JetMetMinDPhiConstructor = lambda : JetMetMinDPhi(jetCollectionName= "Jet", metCollectionName = 'MET') 
 
