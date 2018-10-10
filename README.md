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

# Running instructions:
Structure:

python PhysicsTools/NanoAODTools/scripts/nano_postproc.py $outDir $inputFile -I $locationModules $ModuleName

Example:

python PhysicsTools/NanoAODTools/scripts/nano_postproc.py /eos/user/v/vmilosev/test.root root://gfe02.grid.hep.ph.ic.ac.uk:1097//store/user/bkrikler/ttH_HToInvisible_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1_NanoAOD_1/180530_113050/0000/output_nanoaod_9.root -I  VBFHToInv.NanoAODTools.postprocessing.VBFHToInvModules JetMetMinDPhiConstructor

```


