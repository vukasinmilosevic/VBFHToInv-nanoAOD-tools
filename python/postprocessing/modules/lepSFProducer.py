# -----------------------------------------------------------
#Updated by AMM -- to include other WP and veto efficiencies.
# --- 24/10/2018.
# -----------------------------------------------------------
import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class lepSFProducer(Module):
    def __init__(self, era, muonSelectionTag, electronSelectionTag):

        self.era = era
        #self.inputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/leptonSF" + self.era + "/"
        self.inputFilePath = os.environ['CMSSW_BASE'] + "/src/VBFHToInv/NanoAODTools/data/leptonSF" + self.era + "/"

        self.muonSelectionTag = muonSelectionTag
        self.electronSelectionTag = electronSelectionTag

        mu_f=["RunBCDEF_SF_ID_syst.root","RunBCDEF_SF_ISO_syst.root"]
        mu_type=["ID","ISO"]
        if "Loose" in muonSelectionTag:
            mu_h = ["NUM_LooseID_DEN_genTracks_pt_abseta","NUM_LooseRelIso_DEN_LooseID_pt_abseta"]
        elif "Tight" in muonSelectionTag:
            mu_h = ["NUM_TightID_DEN_genTracks_pt_abseta","NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta"]


        if "withTrg" in muonSelectionTag:
            mu_f.append("Mu_Trg.root")
            mu_h.append("IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio")
            mu_type.append("TRIG")

        el_f = ["egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root","egammaEffi.txt_EGM2D_runBCDEF_passingRECO_lowEt.root"]
        el_h = ["EGamma_SF2D","EGamma_SF2D"]
        el_type=["RECO","RECOlowEt"]
        if electronSelectionTag=="Veto":
            el_f.append("egammaEffi.txt_EGM2D_runBCDEF_passingVeto94X.root")
            el_h.append("EGamma_SF2D")
            el_type.append("IDISO")
        if electronSelectionTag=="Tight":
            el_f.append("egammaEffi.txt_EGM2D_runBCDEF_passingTight94X.root")
            el_h.append("EGamma_SF2D")
            el_type.append("IDISO")




        mu_f = [self.inputFilePath + f for f in mu_f]
        el_f = [self.inputFilePath + f for f in el_f]

        self.mu_f = ROOT.std.vector(str)(len(mu_f))
        self.mu_h = ROOT.std.vector(str)(len(mu_f))
        self.mu_type = ROOT.std.vector(str)(len(mu_type))
        for i in range(len(mu_f)): self.mu_f[i] = mu_f[i]; self.mu_h[i] = mu_h[i]; self.mu_type[i] = mu_type[i];
        self.el_f = ROOT.std.vector(str)(len(el_f))
        self.el_h = ROOT.std.vector(str)(len(el_f))
        self.el_type = ROOT.std.vector(str)(len(el_type))
        for i in range(len(el_f)): self.el_f[i] = el_f[i]; self.el_h[i] = el_h[i]; self.el_type[i] = el_type[i];

        for library in [ "libCondFormatsJetMETObjects", "libVBFHToInvNanoAODTools" ]:
            if library not in ROOT.gSystem.GetLibraries():
                print("Load Library '%s'" % library.replace("lib", ""))
                ROOT.gSystem.Load(library)

    def beginJob(self):
        self._worker_mu = ROOT.LeptonEfficiencyCorrectorCppWorker(self.mu_f,self.mu_h)
        self._worker_el = ROOT.LeptonEfficiencyCorrectorCppWorker(self.el_f,self.el_h)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_effSF_%s"%(self.muonSelectionTag), "F", lenVar="nMuon")
        self.out.branch("Electron_effSF_%s"%(self.electronSelectionTag), "F", lenVar="nElectron")
        for i in range(len(self.mu_type)): 
            self.out.branch("Muon_errSF_%s_%s"%(self.mu_type[i],self.muonSelectionTag), "F", lenVar="nMuon")
        for i in range(len(self.el_type)): 
            self.out.branch("Electron_errSF_%s_%s"%(self.el_type[i],self.electronSelectionTag), "F", lenVar="nElectron")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        sf_el = [ self._worker_el.getSF(el.pdgId,el.pt,el.eta) for el in electrons ]
        sf_mu = [ self._worker_mu.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        self.out.fillBranch("Muon_effSF_%s"%(self.muonSelectionTag), sf_mu)
        self.out.fillBranch("Electron_effSF_%s"%(self.electronSelectionTag), sf_el)
        for i in range(len(self.mu_type)): 
            sf_mu_err = [ self._worker_mu.getSFErr(i,mu.pdgId,mu.pt,mu.eta) for mu in muons ]
            self.out.fillBranch("Muon_errSF_%s_%s"%(self.mu_type[i],self.muonSelectionTag), sf_mu_err)
        for i in range(len(self.el_type)): 
            sf_el_err = [ self._worker_el.getSFErr(i,el.pdgId,el.pt,el.eta) for el in electrons ]
            self.out.fillBranch("Electron_errSF_%s_%s"%(self.el_type[i],self.electronSelectionTag), sf_el_err)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepSFveto = lambda : lepSFProducer( '2017', 'Loose', 'Veto')
#lepSFvetotrig = lambda : lepSFProducer( '2017', 'Loose_withTrg', 'Veto')
lepSFtight = lambda : lepSFProducer( '2017', 'Tight', 'Tight')
