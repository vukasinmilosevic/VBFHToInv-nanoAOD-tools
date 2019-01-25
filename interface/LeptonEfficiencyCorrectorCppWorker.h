#ifndef VBFHToInv_NanoAODTools_LeptonEfficiencyCorrectorCppWorker_h
#define VBFHToInv_NanoAODTools_LeptonEfficiencyCorrectorCppWorker_h

#include <iostream>
#include <string>
#include <vector>
#include <TH2.h>
#include <TFile.h>

#include "PhysicsTools/NanoAODTools/interface/WeightCalculatorFromHistogram.h"

class LeptonEfficiencyCorrectorCppWorker {
 public:

  LeptonEfficiencyCorrectorCppWorker() {effmaps_.clear();}
  LeptonEfficiencyCorrectorCppWorker(const std::vector<std::string> & files, const std::vector<std::string> & histos);
  ~LeptonEfficiencyCorrectorCppWorker() {}

  void setLeptons(int nLep, int *lepPdgId, float *lepPt, float *lepEta);

  float getSF(int pdgid, float pt, float eta);
  float getSFErr(unsigned type, int pdgid, float pt, float eta);
  const std::vector<float> & run();

private:
  std::vector<TH2F*> effmaps_;
  std::vector<float> ret_;
  int nLep_;
  float *Lep_eta_, *Lep_pt_;
  int *Lep_pdgId_;
};

#endif
