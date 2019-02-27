#include "VBFHToInv/NanoAODTools/interface/NLOCorrectorCppWorker.h"

NLOCorrectorCppWorker::NLOCorrectorCppWorker(std::string process, std::vector<std::string>  files)
{

  isQCD_ = false;
  hEWKcorr_ = 0;
  hQCDcorr_ = 0;
  hVBFcorr_.clear();
  hcorr_ = 0;

  nMjjBins_ = 4;
  binMjj_[0] = 200;
  binMjj_[1] = 500;
  binMjj_[2] = 1000;
  binMjj_[3] = 1500;
  binMjj_[4] = 5000;


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
      std::string ewk_histName;
      std::string qcd_histName;
      if (process.find("W")!=process.npos) {
	ewk_histName = "EWKcorr/W";
	qcd_histName = "WJets_012j_NLO/nominal";
      }
      else {
	ewk_histName = "EWKcorr/Z";
	qcd_histName = "ZJets_012j_NLO/nominal";
      }

      if (kfactors->Get(ewk_histName.c_str())) hEWKcorr_ = (TH1F*)(kfactors->Get(ewk_histName.c_str()))->Clone("EWKcorr");//!
      if (kfactors->Get(qcd_histName.c_str())) hQCDcorr_ = (TH1F*)(kfactors->Get(qcd_histName.c_str()))->Clone("QCDcorr");//!
      
      if (hEWKcorr_) hEWKcorr_->SetDirectory(0);
      else {
	std::cout << " -- Problem, histogram " << ewk_histName << " not found !" << std::endl; 
	exit(1);
      }
      if (hQCDcorr_) hQCDcorr_->SetDirectory(0);
      else {
	std::cout << " -- Problem, histogram " << qcd_histName << " not found !" << std::endl; 
	exit(1);
      }

      for (unsigned iB(0); iB<nMjjBins_; ++iB){
	std::ostringstream label,labelSave;
	label << "kfactors_shape/kfactor_vbf_mjj_" 
	      << binMjj_[iB] << "_" 
	      << binMjj_[iB+1] << "_smoothed";
	labelSave << "VBFcorr_" << binMjj_[iB] << "_"  << binMjj_[iB+1];
	if (perproc->Get(label.str().c_str())) hVBFcorr_.push_back((TH1F*)(perproc->Get(label.str().c_str()))->Clone(labelSave.str().c_str()));
	if (hVBFcorr_[iB]) hVBFcorr_[iB]->SetDirectory(0);
	else {
	  std::cout << " -- Problem, histogram " << label.str() << " not found !" << std::endl; 
	  exit(1);
	}
      }

    }

    kfactors->Close();
    perproc->Close();
  } else if (process.find("EWK")!= process.npos){
    if (files.size()!=1) {
      std::cout << " -- Error ! Wrong size for input files: " <<  files.size() << " instead of one." << std::endl;
      exit(1);
    }
    TFile *kfactors = TFile::Open(files[0].c_str(),"read");
    hcorr_ = (TH2F*)(kfactors->Get("TH2F_kFactor"))->Clone("QCDcorr");//!
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

    //find right Mjj bin:
    unsigned iB = 0;
    for (; iB<nMjjBins_; ++iB){
      if (mjj >= binMjj_[iB] && mjj < binMjj_[iB+1])
	{
	  break;
	}
    }
    if (mjj < binMjj_[0]) iB = 0;
    else if (mjj > binMjj_[nMjjBins_]) iB = nMjjBins_-1;
    //std::cout << " Mjj " << mjj << " found bin " << iB << std::endl;
    if (!hVBFcorr_[iB]) {
      std::cerr << " -- Error ! Histo not found, Mjj " << mjj << " bin " << iB << " nMjjBins = " << nMjjBins_ << std::endl;
      exit(1);
    }
    WeightCalculatorFromHistogram vbfCorr(hVBFcorr_[iB]);
    double vbfSF = vbfCorr.getWeight(pT);

    if (qcdSF!=0) nloSF = (ewkSF/qcdSF)*vbfSF;
    
  }
  else {
    WeightCalculatorFromHistogram corr(hcorr_);
    nloSF = corr.getWeight(pT,mjj);
  }
  return nloSF;

}

