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

class bosonDecayFinder(Module):
    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("decayLeptonId", "I")

        self.counter_e = 0
        self.counter_mu = 0
        self.counter_tau = 0
        self.counter_tau_e = 0
        self.counter_tau_mu = 0
        self.counter_tau_had = 0

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print 'Decay to e: %d'%self.counter_e
        print 'Decay to mu: %d'%self.counter_mu
        print 'Decay to tau: %d %d'%(self.counter_tau,self.counter_tau_e+self.counter_tau_mu+self.counter_tau_had)
        print 'Tau Decay to e: %d'%self.counter_tau_e
        print 'Tau Decay to mu: %d'%self.counter_tau_mu
        print 'Tau Decay to hadronic: %d'%self.counter_tau_had

        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        decayLeptonId = 0
        #print ' - event %d:'%(event._entry)

        genParticles =  Collection(event, "GenPart")
        boson_found = False
        for part in genParticles:
            if ( (abs(part.pdgId)>10 and abs(part.pdgId) < 17) and ( (part.status == 1 and (part.statusFlags & 0x1)>0) or ((part.statusFlags & 0x1)>0 and (part.statusFlags & 0x2)>0) ) ):

                if (part.statusFlags & 0x2)>0: 
                    self.counter_tau += 1
                    if (part.pdgId==11 or abs(part.pdgId)==12):
                        self.counter_tau_e += 1
                        decayLeptonId = 3
                    elif (part.pdgId==13 or abs(part.pdgId)==14):
                        self.counter_tau_mu += 1
                        decayLeptonId = 4
                    elif (part.pdgId==15 or abs(part.pdgId)==16):
                        self.counter_tau_had += 1
                        decayLeptonId = 5
                else:
                    if (part.pdgId==11 or abs(part.pdgId)==12):
                        self.counter_e += 1
                        decayLeptonId = 1
                    elif (part.pdgId==13 or abs(part.pdgId)==14):
                        self.counter_mu += 1
                        decayLeptonId = 2


        self.out.fillBranch("decayLeptonId",decayLeptonId)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

bosonDecay = lambda : bosonDecayFinder()
