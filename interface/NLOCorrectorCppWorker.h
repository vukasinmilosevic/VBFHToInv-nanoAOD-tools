#ifndef VBFHToInv_NanoAODTools_NLOCorrectorCppWorker_h
#define VBFHToInv_NanoAODTools_NLOCorrectorCppWorker_h

#include <iostream>
#include <string>
#include <vector>
#include <TH2.h>
#include <TFile.h>

#include "PhysicsTools/NanoAODTools/interface/WeightCalculatorFromHistogram.h"

class NLOCorrectorCppWorker {
 public:

  NLOCorrectorCppWorker() {}
  NLOCorrectorCppWorker(const std::string & process, const std::vector<std::string> & files);
  ~NLOCorrectorCppWorker() {}

  double getSF(const double & pT, const double & mjj);

private:
  bool isQCD_;

  TH1F *hEWKcorr_;
  TH1F *hQCDcorr_;
  TH1F *hVBFcorr_;

  TH2F *hcorr_;
};

#endif
