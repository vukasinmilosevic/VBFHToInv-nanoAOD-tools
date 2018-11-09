import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class TriggerSelection(Module):
    def __init__(self):
        self.HLT_signal_trigger_paths = [
            "HLT_PFMET110_PFMHT110_IDTight",
            "HLT_PFMET120_PFMHT120_IDTight",
            "HLT_PFMET130_PFMHT130_IDTight",
            "HLT_PFMET140_PFMHT140_IDTight",

            "HLT_PFMET100_PFMHT100_IDTight_PFHT60",
            "HLT_PFMET120_PFMHT120_IDTight_PFHT60",

            "HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60",

            "HLT_PFMETTypeOne100_PFMHT100_IDTight_PFHT60",
            "HLT_PFMETTypeOne120_PFMHT120_IDTight_PFHT60",

            "HLT_PFMETTypeOne110_PFMHT110_IDTight",
            "HLT_PFMETTypeOne120_PFMHT120_IDTight",
            "HLT_PFMETTypeOne130_PFMHT130_IDTight",
            "HLT_PFMETTypeOne140_PFMHT140_IDTight",

            "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_PFMETNoMu130_PFMHTNoMu130_IDTight",
            "HLT_PFMETNoMu140_PFMHTNoMu140_IDTight",

            "HLT_PFHT1050",

            "HLT_DiJet110_35_Mjj650_PFMET110",
            "HLT_DiJet110_35_Mjj650_PFMET120",
            "HLT_DiJet110_35_Mjj650_PFMET130",
            "HLT_TripleJet110_35_35_Mjj650_PFMET110",
            "HLT_TripleJet110_35_35_Mjj650_PFMET120",
            "HLT_TripleJet110_35_35_Mjj650_PFMET130",

            "HLT_PFHT500_PFMET100_PFMHT100_IDTight",
            "HLT_PFHT500_PFMET110_PFMHT110_IDTight",
            "HLT_PFHT700_PFMET85_PFMHT85_IDTight",
            "HLT_PFHT700_PFMET95_PFMHT95_IDTight",
            "HLT_PFHT800_PFMET75_PFMHT75_IDTight",
            "HLT_PFHT800_PFMET85_PFMHT85_IDTight",
        ]

        self.HLT_control_trigger_paths = [
            "HLT_IsoMu27",

            "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_PFMETNoMu130_PFMHTNoMu130_IDTight",
            "HLT_PFMETNoMu140_PFMHTNoMu140_IDTight",

            "HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60",

            "HLT_PFHT1050",
        ]


    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        for trigger in self.HLT_signal_trigger_paths + self.HLT_control_trigger_paths:
            try:
                trig_check = getattr(event, trigger)
                if trig_check == 1:
                    return True # event passes selection
            except (AttributeError, RuntimeError), e:
                #Trigger path does not exist in this file
                continue
        return False # if no triggers pass          


TriggerSelectionConstructor = lambda : TriggerSelection()
