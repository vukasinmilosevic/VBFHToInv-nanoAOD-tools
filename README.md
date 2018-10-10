# VBFHToInv-nanoAOD-tools
Additional modules for nanoAODtools specific to the VBF Higgs to invisible analysis.

Fisrt time setup can be found bellow:

## Instructions

```bash
# Setting up the CMSSW environment
source /cvmfs/cms.cern.ch/cmsset_default.sh # !! or .csh
export SCRAM_ARCH=slc6_amd64_gcc630 # !! or setenv SCRAM_ARCH slc6_amd64_gcc630
cmsrel CMSSW_9_4_6_patch1
cd CMSSW_9_4_6_patch1/src/
cmsenv
git cms-init

# combining all repositories of interest
git cms-merge-topic cms-nanoAOD:master
git clone https://github.com/vukasinmilosevic/nanoAOD-tools.git     $CMSSW_BASE/src/PhysicsTools/NanoAODTools
git clone https://github.com/vukasinmilosevic/VBFHToInv-nanoAOD-tools.git $CMSSW_BASE/src/VBFHToInv/NanoAODTools

# compile the thing
cd $CMSSW_BASE/src
scram b -j 16
```


