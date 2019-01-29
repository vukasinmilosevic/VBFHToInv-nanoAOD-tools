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

class nloSFProducer(Module):
    def __init__(self, era, labelsW, labelsDY, labelsZnunu, labelsEWK):

        self.era = era
        self.labelsW = [label for label in labelsW]
        self.labelsDY = [label for label in labelsDY]
        self.labelsZnunu = [label for label in labelsZnunu]
        self.labelsEWK = [label for label in labelsEWK]

        #self.inputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/leptonSF" + self.era + "/"
        self.inputFilePath = os.environ['CMSSW_BASE'] + "/src/VBFHToInv/NanoAODTools/data/nloSF" + self.era + "/"

        for library in [ "libCondFormatsJetMETObjects", "libVBFHToInvNanoAODTools" ]:
            if library not in ROOT.gSystem.GetLibraries():
                print("Load Library '%s'" % library.replace("lib", ""))
                ROOT.gSystem.Load(library)

    def beginJob(self):
        #self._QCDworker = ROOT.NLOCorrectorCppWorker("QCD",self.qcd_nlo_f,self.label_qcd_nlo_f)
        pass

    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.process = 'OTHER'
        self.counter = 0

        qcd_nlo_f=["kfactor_24bins.root"]
        inputFileName = inputFile.GetName()

        for label in self.labelsW:
            if label in inputFileName: 
                self.process = 'QCDW'
                qcd_nlo_f.append("kfactor_VBF_wjet.root")
        for label in self.labelsDY:
            if label in inputFileName: 
                self.process = 'QCDDY'
                qcd_nlo_f.append("kfactor_VBF_zll.root")
        for label in self.labelsZnunu:
            if label in inputFileName: 
                self.process = 'QCDZnunu'
                qcd_nlo_f.append("kfactor_VBF_znn.root")
        for label in self.labelsEWK:
            if label in inputFileName: 
                self.process = label
                if 'EWKW' in label: ewk_nlo_f=["kFactor_WToLNu_pT_Mjj.root"]
                else: ewk_nlo_f=["kFactor_ZToNuNu_pT_Mjj.root"]

        print 'Inputfile: %s, process %s'%(inputFileName,self.process)

        if ('QCD' in self.process or 'EWK' in self.process):
            if 'QCD' in self.process: 
                self.nlo_f = ROOT.std.vector(str)(len(qcd_nlo_f))
                for i in range(len(qcd_nlo_f)): 
                    self.nlo_f[i] = self.inputFilePath + qcd_nlo_f[i]
                    print ' --- Adding file %s'%self.nlo_f[i]
            else: 
                self.nlo_f = ROOT.std.vector(str)(len(ewk_nlo_f))
                for i in range(len(ewk_nlo_f)): 
                    self.nlo_f[i] = self.inputFilePath + ewk_nlo_f[i]
                    print ' --- Adding file %s'%self.nlo_f[i]

            self._worker = ROOT.NLOCorrectorCppWorker(self.process,self.nlo_f)

        else: self._worker = None

        self.out.branch("nloSF_%s"%(self.process), "F")
        self.out.branch("gen_boson_pt", "F")
        self.out.branch("gen_mjj", "F")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print 'Found %d events with boson'%(self.counter)
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        nloSF = 1.0
        boson_pt=0
        mjj=0
        #print ' - event %d:'%(event._entry)

        if self._worker: 

            genParticles =  Collection(event, "GenPart")
            boson_found = False
            lep1 = None
            lep2 = None
            for part in genParticles:
                #if ( (part.pdgId == 23 or abs(part.pdgId) == 24) and (part.statusFlags & 0x2000)>0 and (part.statusFlags & 0x100)>0 ):
                if ( (abs(part.pdgId)>10 and abs(part.pdgId) < 17) and ( (part.status == 1 and (part.statusFlags & 0x1)>0) or ((part.statusFlags & 0x1)>0 and (part.statusFlags & 0x2)>0) ) ):
                    if (part.genPartIdxMother>=0):
                        mother = genParticles[part.genPartIdxMother]
                        #print ' --- event %d pdgid %d --- pdg mother %d: %d '%(event._entry,part.pdgId,part.genPartIdxMother,mother.pdgId)
 
                        if (mother.pdgId == 23 or abs(mother.pdgId) == 24):
                            boson_pt = mother.pt
                            boson_found = True
                        else:
                            if (part.pdgId>0):
                                lep1 = part
                            else:
                                lep2 = part

                    else:
                        #print ' --- event %d pdgid %d --- no mother'%(event._entry,part.pdgId)
                        if (part.pdgId>0):
                            lep1 = part
                        else:
                            lep2 = part

            if (not boson_found and lep1 is not None and lep2 is not None):
                boson_pt = (lep1.p4()+lep2.p4()).Pt()
                boson_found = True

            if (not boson_found):
                idx=0
                print ' --- event %d boson not found:'%(event._entry)
                for part in genParticles:
                    print ' ------ part %d: pdgid %d pT %3.3f status %d flags %d mother %d'%(idx,part.pdgId,part.pt,part.status,part.statusFlags,part.genPartIdxMother)
                    idx += 1

                        #if (part.genPartIdxMother>=0):
                            #print ' ------ pdg mother %d: %d '%(part.genPartIdxMother,genParticles[part.genPartIdxMother].pdgId)



            genJets = Collection(event, "GenJet")
                #idx = 0
                #for genjet in genJets:
                #    print 'Jet %d: pT=%3.3f GeV'%(idx,genjet.pt)
                #    idx += 1
            if (len(genJets)>1):
                mjj = (genJets[0].p4()+genJets[1].p4()).M()
                
            nloSF = self._worker.getSF(boson_pt,mjj)
            if boson_found: self.counter += 1

        self.out.fillBranch("nloSF_%s"%(self.process),nloSF)
        self.out.fillBranch("gen_boson_pt",boson_pt)
        self.out.fillBranch("gen_mjj",mjj)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

nloSF = lambda : nloSFProducer('2016', ["JetsToLNu"], ["JetsToLL"], ["JetsToNuNu"], ["EWKW","EWKZ"])
