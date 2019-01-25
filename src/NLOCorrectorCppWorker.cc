#include "VBFHToInv/NanoAODTools/interface/NLOCorrectorCppWorker.h"

NLOCorrectorCppWorker::NLOCorrectorCppWorker(const std::string & process, const std::vector<std::string> & files)
{

  isQCD_ = false;
  hEWKcorr_ = 0;
  hQCDcorr_ = 0;
  hVBFcorr_ = 0;
  hcorr_ = 0;

  if (process.find("QCD")!= process.npos){
    isQCD_ = true;
    if (files.size()!=2) {
      std::cout << " -- Error ! Wrong size for input files: " <<  files.size() << " instead of two: inclusive and per-process file." << std::endl;
      exit(1);
    }
    TFile *kfactors = TFile::Open(files[0].c_str(),"read");
    TFile *perproc = TFile::Open(files[1].c_str(),"read");
    if(!kfactors || !perproc) {
      if (!kfactors) std::cout << " -- WARNING! File " << files[0] << " cannot be opened. Skipping... " << std::endl;
      if (!perproc) std::cout << " -- WARNING! File " << files[1] << " cannot be opened. Skipping... " << std::endl;
    }
    else {
      if (process.find("W")!=process.npos) {
	hEWKcorr_ = (TH1F*)(kfactors->Get("EWKcorr/W"))->Clone("EWKcorr");
	hQCDcorr_ = (TH1F*)(kfactors->Get("WJets_012j_NLO/nominal"))->Clone("QCDcorr");
      }
      else {
	hEWKcorr_ = (TH1F*)(kfactors->Get("EWKcorr/Z"))->Clone("EWKcorr");
	hQCDcorr_ = (TH1F*)(kfactors->Get("ZJets_012j_NLO/nominal"))->Clone("QCDcorr");
      }

      hVBFcorr_ = (TH1F*)(perproc->Get("kfactors_shape/kfactor_vbf"))->Clone("VBFcorr");

      hEWKcorr_->SetDirectory(0);
      hQCDcorr_->SetDirectory(0);
      hVBFcorr_->SetDirectory(0);

    }

    kfactors->Close();
    perproc->Close();
  } else if (process.find("EWK")!= process.npos){
    if (files.size()!=1) {
      std::cout << " -- Error ! Wrong size for input files: " <<  files.size() << " instead of one." << std::endl;
      exit(1);
    }
    TFile *kfactors = TFile::Open(files[0].c_str(),"read");
    hcorr_ = (TH2F*)(kfactors->Get("TH2F_kFactor"))->Clone("QCDcorr");
    hcorr_->SetDirectory(0);
    kfactors->Close();
  } else {
    std::cerr << " -- Warning ! Unknown production mode, please implement." << std::endl;
  }
}

double NLOCorrectorCppWorker::getSF(const double & pT, const double & mjj) {

  double nloSF =1;
  if (isQCD_){
    WeightCalculatorFromHistogram ewkCorr(hEWKcorr_);
    double ewkSF = ewkCorr.getWeight(pT);
    WeightCalculatorFromHistogram qcdCorr(hQCDcorr_);
    double qcdSF = qcdCorr.getWeight(pT);
    WeightCalculatorFromHistogram vbfCorr(hVBFcorr_);
    double vbfSF = vbfCorr.getWeight(pT);

    if (qcdSF!=0) nloSF = (ewkSF/qcdSF)*vbfSF;

  }
  else {
    WeightCalculatorFromHistogram corr(hcorr_);
    nloSF = corr.getWeight(pT,mjj);
  }
  return nloSF;

}

