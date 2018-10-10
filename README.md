# VBFHToInv-nanoAOD-tools
Additional modules for nanoAODtools specific to the VBF Higgs to invisible analysis.

Fisrt time setup can be found bellow:

## Instructions

```bash
# Setting up the CMSSW environment
cmsrel CMSSW_10_2_5
cd CMSSW_10_2_5/src/
cmsenv

# combining all repositories of interest
git clone https://github.com/vukasinmilosevic/nanoAOD-tools.git     $CMSSW_BASE/src/PhysicsTools/NanoAODTools
git clone https://github.com/vukasinmilosevic/VBFHToInv-nanoAOD-tools.git $CMSSW_BASE/src/VBFHToInv/NanoAODTools

# compile the thing
cd $CMSSW_BASE/src
scram b -j 16
```


