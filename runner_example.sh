#!/usr/bin/bash 
bash 
source /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/dmmc.sh 
echo $LD_LIBRARY_PATH 
echo $PYTHONPATH 
mkdir -p /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400
cd /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400 
python2.7 /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/bin/mg5_aMC /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/F3C_XX_NLO_SMt_MY1000_MX400_topologyinstructions
sleep 5 
python2.7 /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/bin/mg5_aMC /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/F3C_XX_NLO_SMt_MY1000_MX400_runinstructions
sleep 5 
source /cvmfs/sw.hsf.org/spackages7/key4hep-stack/2023-04-08/x86_64-centos7-gcc11.2.0-opt/urwcv/setup.sh 
cd /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15 
python /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/editrecastfile.py -r ./F3C_XX_NLO_SMt_MY1000_MX400_MA5recastinstructions_proto -s /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400/Events/run_01//parton_systematics.log -f parton_systematics 
 python /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/editrecastfile.py -r ./F3C_XX_NLO_SMt_MY1000_MX400_sfsinstructions_proto -s /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400/Events/run_01//parton_systematics.log -f parton_systematics 
 cd /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400
source /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/py3_env3/bin//activate 
echo $SCRAM_ARCH 
cd /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400 
rm madanalysis5 -rf 
git clone https://github.com/MadAnalysis/madanalysis5.git -b v1.10.10 madanalysis5 
cp /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/install_zlib_fix.py /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/madanalysis/install/install_zlib.py 
cd /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5 
mkdir -p tools/PADForSFS 
chmod a+xr tools/PADForSFS 
pwd 
gcc --version 
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.08/x86_64-centos7-gcc48-opt/bin/thisroot.sh 
LD_LIBRARY_PATH=/afs/cern.ch/work/o/oiorio/DMMC/LHAPDFInstall/lib:$LD_LIBRARY_PATH 
LD_LIBRARY_PATH=/tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/SampleAnalyzer/Lib:$LD_LIBRARY_PATH 
LD_LIBRARY_PATH=/tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/SampleAnalyzer/ExternalSymLink/Lib:$LD_LIBRARY_PATH 
LD_LIBRARY_PATH=/tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/delphes:$LD_LIBRARY_PATH 
export LD_LIBRARY_PATH 
ROOT_INCLUDE_PATH=/tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/MA5/madanalysis5/tools/delphes/external:$ROOT_INCLUDE_PATH 
ROOT_INCLUDE_PATH=/tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/delphes/external:$ROOT_INCLUDE_PATH 
export ROOT_INCLUDE_PATH 
python /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/bin/ma5 -s /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/MA5//MA5AuxiliaryFiles/MA5_installpackages_nondelphes 
source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/setup.sh 
source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/bin/thisroot.sh 
python /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/bin/ma5 -s /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/MA5//MA5AuxiliaryFiles/MA5_installpackages_delphes 
python /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/bin/ma5 -s /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/MA5//MA5AuxiliaryFiles/MA5_installpackages_pad_only 
cp /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/MA5//MA5AuxiliaryFiles/run_recast.py /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/madanalysis/misc/ 
cp /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/MA5//MA5AuxiliaryFiles/recast_configuration.py /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/madanalysis/configuration/ 
cp /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/RecastingCards/delphes* /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/PAD/Input/Cards/ 
cp /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/RecastingCards/sfs* /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/PADForSFS/Input/Cards/ 
cp /afs/cern.ch/user/o/oiorio/public/DMMC/atlas_susy_2018_32.info /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/PAD/Build/SampleAnalyzer/User/Analyzer/ 
mv /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/PAD/Build/SampleAnalyzer/User/Analyzer/atlas_susy_2018_32_all.json /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/tools/PAD/Build/SampleAnalyzer/User/Analyzer/atlas_susy_2018_32.json 
pwd 
cp /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/F3C_XX_NLO_SMt_MY1000_MX400_MA5recastinstructions_protofix . 
cp /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/F3C_XX_NLO_SMt_MY1000_MX400_sfsinstructions_protofix . 
python /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/bin/ma5 -R -s ./F3C_XX_NLO_SMt_MY1000_MX400_MA5recastinstructions_protofix 
rm -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400ANALYSIS_0_RecastRun/Output/SAF/*/RecoEvents* 
cp -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/ANALYSIS_0 /eos/home-o/oiorio/DMMC/Events//condor/work/F3C_XX_NLO_SMt_MY1000_MX400_ANALYSIS_0 
cp -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400/Events/run_01/events.lhe.gz /eos/home-o/oiorio/DMMC/Events//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/ 
cp -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400/Events/run_01/unweighted_events.lhe.gz /eos/home-o/oiorio/DMMC/Events//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/ 
cp -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400/Events/run_01_decayed_1/events.lhe.gz /eos/home-o/oiorio/DMMC/Events//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/events_decayed_1.lhe.gz 
cp -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400/Events/run_01/summary.txt /eos/home-o/oiorio/DMMC/Events//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/ 
cp -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400/Events/run_01/parton_systematics.log /eos/home-o/oiorio/DMMC/Events//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/ 
cp -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400/Events/run_01_decayed_01/run_01_decayed_1_tag_1_banner.txt /eos/home-o/oiorio/DMMC/Events//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/ 
python /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/bin/ma5 -s ./F3C_XX_NLO_SMt_MY1000_MX400_sfsinstructions_protofix 
rm -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/ANALYSIS_1/Output/SAF/*/lheEvents0_0/ma5_events.lhe* 
cp -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400/madanalysis5/ANALYSIS_1 /eos/home-o/oiorio/DMMC/Events//condor/work/F3C_XX_NLO_SMt_MY1000_MX400_ANALYSIS_1 
cd /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400 
python /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/cleardir.py -d ./ -f DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1000_MX400 -p 'DMtsimp/MG5Runs/' 
sleep 10 
rm -rf /tmp/mjf-oiorio//condor/work/F3C_XX_NLO_SMt_MY1000_MX400 
