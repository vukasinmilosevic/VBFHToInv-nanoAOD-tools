import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from VBFHToInv.NanoAODTools.postprocessing.modules.dijetVar import DiJetVariables
from VBFHToInv.NanoAODTools.postprocessing.modules.MetCleaning import  MetCleaningProcedure
from VBFHToInv.NanoAODTools.postprocessing.modules.jetMetmindphi import  FormJetMetMinDphi

class JetCleaning(Module):
    def __init__(self, jetCollectionName, lepMCollectionName, lepECollectionName, photonCollectionName, outCollectionName, dR_min):
        self.jetCollectionName = jetCollectionName
        self.lepECollectionName = lepECollectionName
        self.lepMCollectionName = lepMCollectionName
        self.photonCollectionName = photonCollectionName
        self.outCollectionName = outCollectionName
        self.dR_min = dR_min
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
        self.out.branch("leading_Mjj",  "F");
        self.out.branch("leading_dEtajj", "F");
        self.out.branch("leading_dPhijj", "F");
        self.out.branch("MetNoMu_pt", "F");
        self.out.branch("MetNoMu_phi", "F");
        self.out.branch("MetNoEl_pt", "F");
        self.out.branch("MetNoEl_phi", "F");
        self.out.branch("MetNoLep_pt", "F");
        self.out.branch("MetNoLep_phi", "F");
        self.out.branch("jetmet_nomu_mindphi","F");
        self.out.branch("jetmet_noel_mindphi","F")
        self.out.branch("jetmet_nolep_mindphi","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, self.jetCollectionName)
        muons = Collection(event, self.lepMCollectionName)
        electrons = Collection(event, self.lepECollectionName)
        photons = Collection(event, self.photonCollectionName)
        cleanJets_pt = []
        cleanJets_eta = []
        cleanJets_phi = []
        cleanJets_mass = []

        for jet in jets:
  	   test = True
           for muon in muons:
              if (deltaR(jet.eta, jet.phi, muon.eta, muon.phi)< self.dR_min):
                 test =False
           for electron in electrons:
              if (deltaR(jet.eta, jet.phi, electron.eta, electron.phi)< self.dR_min):
                 test =False
          # for photon in photons:
           #   if (deltaR(jet.eta, jet.phi, photon.eta, photon.phi)< self.dR_min):
            #     test =False

           if test:
             cleanJets_pt.append(jet.pt)
             cleanJets_eta.append(jet.eta)
             cleanJets_phi.append(jet.phi)
             cleanJets_mass.append(jet.mass) 
        
        Event_ok_cleanJets, leading_Mjj, leading_dPhijj, leading_dEtajj = DiJetVariables(cleanJets_pt, cleanJets_eta, cleanJets_phi, cleanJets_mass)
       
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        met = Object(event, "MET")
        met_phi = met.phi
        met_pt = met.pt
                 
        Event_ok_cleanMet_electrons, CleanMet_electrons_pt, CleanMet_electrons_phi = MetCleaningProcedure(met_pt, met_phi, electrons)
        Event_ok_cleanMet_muons, CleanMet_muons_pt, CleanMet_muons_phi =  MetCleaningProcedure(met_pt, met_phi, muons) 
        Event_ok_cleanMet_leptons, CleanMet_leptons_pt, CleanMet_leptons_phi =  MetCleaningProcedure(CleanMet_muons_pt,CleanMet_muons_phi, electrons)
        Event_ok_jet_met_Nomu, MinDPhiJMet_Nomu = FormJetMetMinDphi(CleanMet_muons_phi, cleanJets_phi, len(cleanJets_phi))
        Event_ok_jet_met_Noel, MinDPhiJMet_Noel = FormJetMetMinDphi(CleanMet_electrons_phi, cleanJets_phi,len(cleanJets_phi))
        Event_ok_jet_met_Nolep, MinDPhiJMet_Nolep = FormJetMetMinDphi(CleanMet_leptons_phi, cleanJets_phi,len(cleanJets_phi)) 
    
        selection = len(cleanJets_pt)>=2 and leading_Mjj>300 and leading_dEtajj>1 and MinDPhiJMet_Nolep>0.5 and CleanMet_leptons_pt>150
       # selection = True

        if Event_ok_cleanJets and Event_ok_cleanMet_electrons and Event_ok_cleanMet_muons and Event_ok_jet_met_Nomu and Event_ok_jet_met_Noel and Event_ok_cleanMet_leptons and Event_ok_jet_met_Nolep  and selection:
            self.out.fillBranch(self.outCollectionName+"_pt", cleanJets_pt)
            self.out.fillBranch(self.outCollectionName+"_eta", cleanJets_eta)
            self.out.fillBranch(self.outCollectionName+"_phi", cleanJets_phi)
            self.out.fillBranch(self.outCollectionName+"_mass", cleanJets_mass)
            self.out.fillBranch("leading_Mjj", leading_Mjj)
            self.out.fillBranch("leading_dPhijj", leading_dPhijj)
            self.out.fillBranch("leading_dEtajj", leading_dEtajj)
            self.out.fillBranch("MetNoMu_pt", CleanMet_muons_pt)
            self.out.fillBranch("MetNoMu_phi", CleanMet_muons_phi)
            self.out.fillBranch("MetNoEl_pt", CleanMet_electrons_pt)
            self.out.fillBranch("MetNoEl_phi", CleanMet_electrons_phi)
            self.out.fillBranch("MetNoLep_pt", CleanMet_leptons_pt)
            self.out.fillBranch("MetNoLep_phi", CleanMet_leptons_phi)
            self.out.fillBranch("jetmet_nomu_mindphi", MinDPhiJMet_Nomu)
            self.out.fillBranch("jetmet_noel_mindphi", MinDPhiJMet_Noel)
            self.out.fillBranch("jetmet_nolep_mindphi",MinDPhiJMet_Nolep)
            return True
        else:
            return False


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

JetCleaningConstructor = lambda : JetCleaning(jetCollectionName= "Jet", lepMCollectionName = 'Muon', lepECollectionName = 'Electron', photonCollectionName = 'Photon', outCollectionName = "CleanJet", dR_min = 0.4) 
 
