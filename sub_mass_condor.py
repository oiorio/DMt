import os
import optparse
import shutil

usage = 'python sub_mass_condor.py -o out_work_dir -w work_dir -n dryrun -r True' 
parser = optparse.OptionParser(usage)
#parser.add_option('-o','--output', dest='out_store_dir',type=str,default='/eos/home-o/oiorio/DMMC/XSecs',help='file storage directory')
#parser.add_option('-w','--work', dest='work_dir',type=str,default='/eos/home-o/oiorio/DMMC/Events',help='work directory')

parser.add_option('-o','--output', dest='out_store_dir',type=str,default='/eos/home-o/oiorio/DMMC/Events',help='file storage directory')
parser.add_option('-w','--work', dest='work_dir',type=str,default='/tmp/mjf-oiorio/',help='work directory')

parser.add_option('-r','--resubmit_failed', dest='resubmit_failed', type=int, default = 1, help="resubmit failed files in the out_store_dir or work_dir. Suggested option as it will also submit new jobs")
parser.add_option('-n','--dryrun', dest='dryrun', default = False, action='store_true', help="dryrun")
parser.add_option('-g','--group', dest='grouprun', default = False, action='store_true', help="group several runs together")
parser.add_option('-c','--clear', dest='clear', default = False, action='store_true', help="clear the directories from heavy files")
parser.add_option('--forceclear', dest='forceclear', default = False, action='store_true', help="clear the directory from heavy files regardless of the success state")
parser.add_option('--nosubmit', dest='nosubmit', default = False, action='store_true', help="create the cfg files but do not sobmit the jobs")
parser.add_option('-m','--minimum', dest='minimum',type=int,default=2,help="minimum mass point (*200), default =2 (=400),")
parser.add_option('-M','--maximum', dest='maximum',type=int,default=2,help="maximum mass point (*200), default =10-1 (=1800),")
parser.add_option('-f','--force', dest='force', default = False, action='store_true', help="force running on condor even if the directory is there")
parser.add_option('-t','--test', dest='test', default = False, action='store_true', help="run on a test file only")

parser.add_option('--model', dest='model',type=str,default='f3c_yyqcd_nlo',help='model to run')


(opt, args) = parser.parse_args()


out_store_dir=opt.out_store_dir#"/eos/home-o/oiorio/DMMC/XSecs"
work_dir=opt.work_dir
doresub=opt.resubmit_failed
doforce=opt.force

models_f3c_yyqcd_nlo={"F3C_YYQCD_NLO_SMt":("F3C_YYQCD_NLO_SMt_MY1300_MX900_topologyinstructions","F3C_YYQCD_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/F3C_YYQCD_NLO_SMt_MY1300_MX900","mx":"MXc","my":"MYF3u3"},
                             "F3C_YYQCD_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as F3C_YYQCD_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/RecastingCards/recasting_card_2023.dat","xs2":"set F3S_YYQCD_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"F3C_YYQCD_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}

models_f3c_xx_nlo={"F3C_XX_NLO_SMt":("F3C_XX_NLO_SMt_MY1300_MX900_topologyinstructions","F3C_XX_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/F3C_XX_NLO_SMt_MY1300_MX900","mx":"MXc","my":"MYF3u3"},
                             "F3C_XX_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as F3C_XX_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /scratch/lp1c12/DMtsimp_project/DMspin/DMtsimp/core/Cards/recasting_card_2023.dat","xs2":"set F3C_XX_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"F3C_XX_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}

models_f3s_xx_nlo={"F3S_XX_NLO_SMt":("F3S_XX_NLO_SMt_MY1300_MX900_topologyinstructions","F3S_XX_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/F3S_XX_NLO_SMt_MY1300_MX900","mx":"MXs","my":"MYF3u3"},
                             "F3S_XX_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as F3S_XX_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /scratch/lp1c12/DMtsimp_project/DMspin/DMtsimp/core/Cards/recasting_card_2023.dat","xs2":"set F3S_XX_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"F3S_XX_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}

models_f3s_xx_lo={"F3S_XX_LO_SMt":("F3S_XX_LO_SMt_MY1300_MX900_topologyinstructions","F3S_XX_LO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/F3S_XX_LO_SMt_MY1300_MX900","mx":"MXs","my":"MYF3u3"},
                             "F3S_XX_LO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as F3S_XX_LO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /scratch/lp1c12/DMtsimp_project/DMspin/DMtsimp/core/Cards/recasting_card_2023.dat","xs2":"set F3S_XX_LO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"F3S_XX_LO_SMt_MY1300_MX900_sfsinstructions_proto")}

#f3v
models_f3v_yyqcd_nlo={"F3V_YYQCD_NLO_SMt":("F3V_YYQCD_NLO_SMt_MY1300_MX900_topologyinstructions","F3V_YYQCD_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/F3V_YYQCD_NLO_SMt_MY1300_MX900","mx":"MXv","my":"MYF3u3"},
                             "F3V_YYQCD_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as F3V_YYQCD_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/RecastingCards/recasting_card_2023.dat","xs2":"set F3V_YYQCD_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"F3V_YYQCD_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}

models_f3v_xx_nlo={"F3V_XX_NLO_SMt":("F3V_XX_NLO_SMt_MY1300_MX900_topologyinstructions","F3V_XX_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/F3V_XX_NLO_SMt_MY1300_MX900","mx":"MXv","my":"MYF3u3"},
                             "F3V_XX_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as F3V_XX_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /scratch/lp1c12/DMtsimp_project/DMspin/DMtsimp/core/Cards/recasting_card_2023.dat","xs2":"set F3V_XX_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"F3V_XX_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}


#f3w
models_f3w_yyqcd_nlo={"F3W_YYQCD_NLO_SMt":("F3W_YYQCD_NLO_SMt_MY1300_MX900_topologyinstructions","F3W_YYQCD_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/F3W_YYQCD_NLO_SMt_MY1300_MX900","mx":"MXw","my":"MYF3u3"},
                             "F3W_YYQCD_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as F3W_YYQCD_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/RecastingCards/recasting_card_2023.dat","xs2":"set F3W_YYQCD_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"F3W_YYQCD_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}

models_f3w_xx_nlo={"F3W_XX_NLO_SMt":("F3W_XX_NLO_SMt_MY1300_MX900_topologyinstructions","F3W_XX_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/F3W_XX_NLO_SMt_MY1300_MX900","mx":"MXw","my":"MYF3u3"},
                             "F3W_XX_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as F3W_XX_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /scratch/lp1c12/DMtsimp_project/DMspin/DMtsimp/core/Cards/recasting_card_2023.dat","xs2":"set F3W_XX_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"F3W_XX_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}




#s3d
models_s3d_yyqcd_nlo={"S3D_YYQCD_NLO_SMt":("S3D_YYQCD_NLO_SMt_MY1300_MX900_topologyinstructions","S3D_YYQCD_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/S3D_YYQCD_NLO_SMt_MY1300_MX900","mx":"MXd","my":"MYS3u3"},
                             "S3D_YYQCD_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as S3D_YYQCD_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/RecastingCards/recasting_card_2023.dat","xs2":"set S3D_YYQCD_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"S3D_YYQCD_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}

models_s3d_xx_nlo={"S3D_XX_NLO_SMt":("S3D_XX_NLO_SMt_MY1300_MX900_topologyinstructions","S3D_XX_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/S3D_XX_NLO_SMt_MY1300_MX900","mx":"MXd","my":"MYS3u3"},
                             "S3D_XX_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as S3D_XX_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /scratch/lp1c12/DMtsimp_project/DMspin/DMtsimp/core/Cards/recasting_card_2023.dat","xs2":"set S3D_XX_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"S3D_XX_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}



#s3m
models_s3m_yyqcd_nlo={"S3M_YYQCD_NLO_SMt":("S3M_YYQCD_NLO_SMt_MY1300_MX900_topologyinstructions","S3M_YYQCD_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/S3M_YYQCD_NLO_SMt_MY1300_MX900","mx":"MXw","my":"MYF3u3"},
                             "S3M_YYQCD_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as S3M_YYQCD_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/RecastingCards/recasting_card_2023.dat","xs2":"set F3S_YYQCD_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"S3M_YYQCD_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}

models_s3m_xx_nlo={"S3M_XX_NLO_SMt":("S3M_XX_NLO_SMt_MY1300_MX900_topologyinstructions","S3M_XX_NLO_SMt_MY1300_MX900_runinstructions",
                             {"out":"output DMtsimp/MG5Runs/S3M_XX_NLO_SMt_MY1300_MX900","mx":"MXw","my":"MYF3u3"},
                             "S3M_XX_NLO_SMt_MY1300_MX900_MA5recastinstructions_proto",{"imp":"import /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/","imp2":"import PYTHIAFILE as S3M_XX_NLO_SMt_MY1300_MX900","imp3":"set main.recast.card_path = /scratch/lp1c12/DMtsimp_project/DMspin/DMtsimp/core/Cards/recasting_card_2023.dat","xs2":"set S3M_XX_NLO_SMt_MY1300_MX900.xsection = SED_CROSSSECTION" },"S3M_XX_NLO_SMt_MY1300_MX900_sfsinstructions_proto")}





models={}
if opt.model=="f3c_yyqcd_nlo":
    models=models_f3c_yyqcd_nlo
    from success_mass_pairs_f3c_yyqcd_nlo import successful_pairs
if opt.model=="f3c_xx_nlo":
    models=models_f3c_xx_nlo
    if(os.path.exists("success_mass_pairs_f3c_xx_nlo.py") ): 
       from success_mass_pairs_f3c_xx_nlo import successful_pairs
    else:
       successful_pairs={"F3C_XX_NLO_SMt":[]}
if opt.model=="f3s_xx_nlo":
    models=models_f3s_xx_nlo
    if(os.path.exists("success_mass_pairs_f3s_xx_nlo.py") ): 
       from success_mass_pairs_f3s_xx_nlo import successful_pairs
    else:
       successful_pairs={"F3S_XX_NLO_SMt":[]}
if opt.model=="f3s_xx_lo":
    models=models_f3s_xx_lo
    from success_mass_pairs_f3s_xx_lo import successful_pairs

#f3v
if opt.model=="f3v_xx_nlo":
    models=models_f3v_xx_nlo
    if(os.path.exists("success_mass_pairs_f3v_xx_nlo.py") ): 
       from success_mass_pairs_f3v_xx_nlo import successful_pairs
    else:
       successful_pairs={"F3V_XX_NLO_SMt":[]}
if opt.model=="f3v_yyqcd_nlo":
    models=models_f3v_yyqcd_nlo
    if(os.path.exists("success_mass_pairs_f3v_yyqcd_nlo.py") ): 
       from success_mass_pairs_f3v_yyqcd_nlo import successful_pairs
    else:
       successful_pairs={"F3V_YYQCD_NLO_SMt":[]}
#f3w
if opt.model=="f3w_xx_nlo":
    models=models_f3w_xx_nlo
    if(os.path.exists("success_mass_pairs_f3w_xx_nlo.py") ): 
       from success_mass_pairs_f3w_xx_nlo import successful_pairs
    else:
       successful_pairs={"F3W_XX_NLO_SMt":[]}
if opt.model=="f3w_yyqcd_nlo":
    models=models_f3w_yyqcd_nlo
    if(os.path.exists("success_mass_pairs_f3w_yyqcd_nlo.py") ): 
       from success_mass_pairs_f3w_yyqcd_nlo import successful_pairs
    else:
       successful_pairs={"F3W_YYQCD_NLO_SMt":[]}


#s3d
if opt.model=="s3d_xx_nlo":
    models=models_s3d_xx_nlo
    if(os.path.exists("success_mass_pairs_s3d_xx_nlo.py") ): 
       from success_mass_pairs_s3d_xx_nlo import successful_pairs
    else:
       successful_pairs={"S3D_XX_NLO_SMt":[]}
if opt.model=="s3d_yyqcd_nlo":
    models=models_s3d_yyqcd_nlo
    if(os.path.exists("success_mass_pairs_s3d_yyqcd_nlo.py") ): 
       from success_mass_pairs_s3d_yyqcd_nlo import successful_pairs
    else:
       successful_pairs={"S3D_YYQCD_NLO_SMt":[]}


#s3m
if opt.model=="s3m_xx_nlo":
    models=models_s3m_xx_nlo
    if(os.path.exists("success_mass_pairs_s3m_xx_nlo.py") ): 
       from success_mass_pairs_s3m_xx_nlo import successful_pairs
    else:
       successful_pairs={"S3M_XX_NLO_SMt":[]}
if opt.model=="s3m_yyqcd_nlo":
    models=models_s3m_yyqcd_nlo
    if(os.path.exists("success_mass_pairs_s3m_yyqcd_nlo.py") ): 
       from success_mass_pairs_s3m_yyqcd_nlo import successful_pairs
    else:
       successful_pairs={"S3M_YYQCD_NLO_SMt":[]}


#from success_mass_pairs_f3s_xx import successful_pairs
print("models are"), models



YMasses=[1800]
XMasses=[900,1100,1300]
XMasses=[1100,900]
XMasses=[1100,900]

YMasses=[1300]
XMasses=[500]
YMasses=[3000]
#XMasses=[2000]
XMasses=[2200]

fullloop = True
fullloop = False
fullloop= not opt.test

FailMassPairs=[]
FailMadanPairs=[]
SuccessMassPairs=[]


Min = opt.minimum 
Max = opt.maximum
if(fullloop):
    YMasses=[i*200 for i in range(Min,Max)]
#    YMasses=[i*200 for i in range(10,14)]
#    YMasses=[i*200 for i in range(13,16)]
#    YMasses=[i*200 for i in range(2,16)]
    XMasses=[1,10,50,100]
    XMasses.extend([i*200 for i in range(1,16)])
mTop=172
nremovedfortop=0
dir_evts_pythia_point=""
if (doresub):
    for m in models:
        for mY in YMasses:
            for mX in XMasses:
                if(mX>mY):continue
                if(mX==mY):mX=mY-5
                if( ( "YYQCD" in m ) and  mY-mX<mTop):
                    nremovedfortop+=1
                    continue
                MX="MX"+str(mX)
                MY="MY"+str(mY)
                fullname=m+"_"+MY+"_"+MX
                dir_point=out_store_dir+"/condor/work/"+fullname
                dirhappened = os.path.exists(dir_point+"_ANALYSIS_0")
                point_failed=True
                hepmc_failed=True
                analhappened=False
                if("YYQCD" in m):
                    dir_evts_pythia=dir_point+"/DMtsimp/MG5Runs/"+fullname+"/Events/run_01_decayed_1/events_PYTHIA8_0.hepmc.gz"
                if("XX" in m):
                    dir_evts_pythia=dir_point+"/DMtsimp/MG5Runs/"+fullname+"/Events/run_01/tag_1_pythia8_events.hepmc.gz"
                dir_evts_pythia_point=dir_evts_pythia
                print("MY= ", MY, " MX= ",MX," dir evts pythia at mass ",dir_evts_pythia_point)
                if(dirhappened):
                    print(" point ",fullname, " happened at ",dir_point)
                    anal_evts=dir_point+"_ANALYSIS_0/Output/SAF/CLs_output_summary.dat"
                    dir_evts=dir_point+"/summary.txt"
                    
                    #anal_evts=dir_point+"/madanalysis5/ANALYSIS_0/Output/SAF/CLs_output_summary.dat"
                    #dir_evts=dir_point+"/DMtsimp/MG5Runs/"+fullname+"/Events/run_01/summary.txt"

                    evtshappened=os.path.exists(dir_evts)
                    analhappened=os.path.exists(anal_evts)
                    print(" analysis dir: " ,anal_evts,"analysis happened?",analhappened)    
                    evtshappened=evtshappened and os.path.exists(dir_evts_pythia)
                    if (evtshappened):
                        hepmc_failed=False
                    print(" events dir: " ,dir_evts_pythia,"events happened?",evtshappened)    

                    dir_evts_madanal=dir_point+"/ANALYSIS_1"
                    evtshappened= os.path.exists(dir_evts_madanal)
                    if(analhappened):
                        print(" point ",fullname, " ran events at ",dir_evts)
                        os.system("tail -20 "+dir_evts)
                        point_failed=False
                if(not analhappened):
                    if(hepmc_failed):
                        FailMassPairs.append((mY,mX))
                    if(point_failed):
                        FailMadanPairs.append((mY,mX))
                if(analhappened):
                    print ("success " , (mY,mX)," |||||||||" )
                    SuccessMassPairs.append((mY,mX))

print("Failed mass pairs are: ",FailMassPairs )
print("n Failed masses: ",len(FailMassPairs) )
print("Failed madanpairs are: ",FailMadanPairs )
print("n Failed madan: ",len(FailMadanPairs) )
print("n Removed for mX-mY>mTop  : ",nremovedfortop)
print(" mass list length ")



#XMasses=[1300]
nevents="1000"
if (fullloop):
    nevents="100000"
#    nevents="1000"
nToRun=0
for m in models:
    string_cfg=""
    string_generate_cfg=""
    string_recast_cfg=""
    string_sfs_cfg=""
    runmg_cfg= open(models[m][0])
    runmg_generate_cfg= open(models[m][1])
    runmg_recast_cfg= open(models[m][3])
    runmg_sfs_cfg= open(models[m][5])

    for l in runmg_cfg.readlines():
        string_cfg=string_cfg+l+""

    for l in runmg_generate_cfg.readlines():
        string_generate_cfg=string_generate_cfg+l+""

    for l in runmg_recast_cfg.readlines():
        string_recast_cfg=string_recast_cfg+l+""

    for l in runmg_sfs_cfg.readlines():
        string_sfs_cfg=string_sfs_cfg+l+""

    print("default cfg is: ")
    print(string_cfg)
    print("default cfg generate is: ")
    print(string_generate_cfg)
    print("default cfg recast is: ")
    print(string_recast_cfg)
    print("default cfg sfs is: ")
    print(string_sfs_cfg)

    
    
    for mY in YMasses:
        for mX in XMasses:
            if(mX>mY):continue
            if(mX==mY):mX=mY-5
            MX="MX"+str(mX)
            MY="MY"+str(mY)
            torun=(not doresub)
            fullname=m+"_"+MY+"_"+MX
            #torun=True
            has_hepmc=True


            mode="M"
            if(doresub):
                if((mY,mX) in FailMassPairs and not ( ( (mY,mX) in SuccessMassPairs ) or ( (mY,mX) in successful_pairs) ) ):
                    torun=True
                    print("running failed mass - hepmc step ",MY,MX)
                    rmdircmd= "rm "+ out_store_dir+"/condor/work/"+fullname+" -rf "
                    print("emptying the folder before launching: ", rmdircmd)
                    if not opt.dryrun:
                        print()
                        #os.system(rmdircmd)
                    has_hepmc=False
                    mode="GM"
                if( (mY,mX) in FailMadanPairs and not ( ( (mY,mX) in SuccessMassPairs ) or ( (mY,mX) in successful_pairs) ) ):
                    torun=True
                    print("running failed mass -madan step ",MY,MX)
                    rmdircmd= "rm "+ out_store_dir+"/condor/work/"+fullname+"/madanalysis5 -rf "
                    rmdircmdt= "rm "+ out_store_dir+"/condor/work/"+fullname+"/tools -rf "
                    rmdircmdf= "rm "+ out_store_dir+"/condor/work/"+fullname+"/*protofix -rf "
                    print("emptying the folder before launching: ", rmdircmd)

                    if not opt.dryrun:
                        print()
                        os.system(rmdircmd)
                        os.system(rmdircmdt)
                        os.system(rmdircmdf)
            toclear=False
            if ( (mY,mX) in SuccessMassPairs ) or (mY,mX) in successful_pairs[m]:
                if ( (mY,mX) in successful_pairs[m] ):
                    print(" successful pair ",mY,mX," imported from repo")
                torun=False
                toclear=True
            if opt.forceclear:
                torun=True
            runmg_name=(models[m][0].replace("MY1300",MY).replace("MX900",MX))
            runmg_generate_name=(models[m][1]).replace("MY1300",MY).replace("MX900",MX)
            runmg_recast_name=(models[m][3]).replace("MY1300",MY).replace("MX900",MX)
            runmg_sfs_name=(models[m][5].replace("MY1300",MY).replace("MX900",MX))
           
            if(torun or doforce):
                print("ready to run mass ",MY,MX)
                print (" mode is ",mode)
                nToRun=nToRun+1
            
            if opt.dryrun:
                print(" dryrun selected! Not actually running.")

                
            if( (torun or doforce ) and not opt.dryrun):
                print ("mx and my are ",mX,mY," runmg name ",runmg_name," generate name ",runmg_generate_name, " recast name ", runmg_recast_name, " sfs name ", runmg_sfs_name)

                os.system("rm "+ runmg_name)
                os.system("rm "+ runmg_generate_name)
                os.system("rm "+ runmg_recast_name)
                os.system("rm "+ runmg_sfs_name)

                runmg_cfg_mxmy=open(runmg_name,"w")
                runmg_generate_cfg_mxmy=open(runmg_generate_name,"w")
                runmg_recast_cfg_mxmy=open(runmg_recast_name,"w")
                runmg_sfs_cfg_mxmy=open(runmg_sfs_name,"w")
            

                outsentence=models[m][2]["out"] 
                rn_new=string_cfg
                outreplace=outsentence.replace("MX900",MX).replace("MY1300",MY)
                print(outsentence,outreplace)
                rn_new=rn_new.replace(outsentence,outreplace)
                runmg_cfg_mxmy.write(rn_new)
                runmg_cfg_mxmy.close()


                mxsentence="set "+ models[m][2]["mx"] +" = 900"
                mysentence="set "+ models[m][2]["my"] +" = 1300"
                launchsentence=models[m][2]["out"].replace("output","launch")
                launchreplace=launchsentence.replace("MX900",MX).replace("MY1300",MY)
                print(launchsentence,launchreplace)


                evsentence="set nevents=1000"
                sg_new= string_generate_cfg
                sg_new=sg_new.replace(launchsentence,launchreplace)
                sg_new=sg_new.replace(mxsentence,mxsentence.replace("900",str(mX)))
                sg_new=sg_new.replace(mysentence,mysentence.replace("1300",str(mY)))
                sg_new=sg_new.replace(evsentence,evsentence.replace("1000",nevents))
                runmg_generate_cfg_mxmy.write(sg_new)
                runmg_generate_cfg_mxmy.close()
            
                impsentence=models[m][4]["imp"] 
                dir_point=work_dir+"/condor/work/"+fullname+"/"
                #out_dir_point=out_store_dir+"/condor/work/"+fullname+"/"
                if("YY" in m):
                    dir_evts_pythia=dir_point+"/DMtsimp/MG5Runs/"+fullname+"/Events/run_01_decayed_1/events_PYTHIA8_0.hepmc.gz"
                if("XX" in m):
                    dir_evts_pythia=dir_point+"/DMtsimp/MG5Runs/"+fullname+"/Events/run_01/tag_1_pythia8_events.hepmc.gz"
                dir_evts_pythia_point=dir_evts_pythia
                print("m= ", m," MY= ", MY, " MX= ",MX," dir evts pythia at mass ",dir_evts_pythia_point)
                impreplace=impsentence.replace(impsentence,"import "+dir_point)
                
                impsentence2=models[m][4]["imp2"].replace("MY1300",MY).replace("MX900",MX)
                print("impsent 2 is ",impsentence2," dir_evts ",dir_evts_pythia_point)
                impreplace2=impsentence2.replace(impsentence2,"import "+dir_evts_pythia_point+" as "+fullname)

                impsentence3=models[m][4]["imp3"] 
                impreplace3=impsentence3.replace(impsentence3,"set main.recast.card_path = /afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/RecastingCards/recasting_card_2023.dat")

                sr_new= string_recast_cfg
                sr_new= sr_new.replace("MY1300",MY).replace("MX900",MX)
                sr_new = sr_new.replace(impsentence,impreplace) 
                sr_new = sr_new.replace(impsentence2,impreplace2) 
                sr_new= sr_new.replace(impsentence3,impreplace3)
                runmg_recast_cfg_mxmy.write(sr_new)
                runmg_recast_cfg_mxmy.close()


                sfs_new = string_sfs_cfg
                sfs_new = sfs_new.replace("MY1300",MY).replace("MX900",MX)
                sfs_new = sfs_new.replace(impsentence2,impreplace2) 
                sfs_new= sfs_new.replace(impsentence3,impreplace3)

                runmg_sfs_cfg_mxmy.write(sfs_new)
                runmg_sfs_cfg_mxmy.close()

                
            local_out_dir=models[m][2]["out"].replace("output","").replace(" ","")
            print("file is ")
            #print("local_out_dir ",type(local_out_dir))
            local_out_dir=local_out_dir.replace("MX900",MX).replace("MY1300",MY)
            #out_store_dir_local=out_store_dir+"/eos/home-o/oiorio/DMMC/XSecs/"+local_out_dir
            #            out_store_dir_local=out_store_dir+"/eos/home-o/oiorio/DMMC/XSecs/"+local_out_dir
            if(opt.clear or opt.forceclear ):
                mode = "C"
##                if opt.forceclear
#                mode = "CC"
                if(toclear):
                    print(" clearing mass point mY ",mY, " mX ",mX)
            command_sub =" python submit_condor.py -m "+mode+" -r "+ runmg_name +" -g " +runmg_generate_name + " -R " + runmg_recast_name + " -S "+ runmg_sfs_name + " -O "+ local_out_dir + " -o " + out_store_dir + " -l " +m+"_"+MY+"_"+MX+" & "
            print ("command submit is: ",command_sub)
            if( (torun or doforce ) and not opt.dryrun):
                print()
                if( torun or toclear or doforce ):
                    print(" running! ",MY,MX )
                    if (not opt.nosubmit): os.system(command_sub)
                    
print(" points list length ",nToRun)
print(" failed mg5 pairs ",FailMassPairs)
FailMadanOnlyPairs=[]
for fa in FailMadanPairs:
    if not fa in FailMassPairs:
        FailMadanOnlyPairs.append(fa)
print(" failed madan only pairs ",FailMadanOnlyPairs)
print(" successful pairs ",SuccessMassPairs)
print(" n successful pairs ",len(SuccessMassPairs))

shutil.copy("success_mass_pairs.py","success_mass_pairs_backup.py")

fos = open("success_mass_pairs.py","w")
fos.write("successful_pairs ={} \n")

#fos.write('successful_pairs["F3C_XX_NLO_SMt"]=[]\n') 
#fos.write('successful_pairs["F3C_XX_LO_SMt"]=[]\n')
#fos.write('successful_pairs["F3C_YYQCD_NLO_SMt"]=[]\n')


for m in models:
    fos.write('successful_pairs[\"'+m+'\"]=')
    print( " pre succ pair ", successful_pairs[m], " \\ len ", len(successful_pairs[m]))
    for S in SuccessMassPairs:
        if not (S in successful_pairs[m]):
            print(" adding ", S, " to successful pair list \\\ ")
            successful_pairs[m].append(S)
    #for S2 in successful_pairs:
    fos.write(str(successful_pairs[m]))

    print( " post succ pair ", successful_pairs[m], " \\ len ", len(successful_pairs[m]))
    fos.write("\n")

    fos.close()
    if(opt.model == "f3c_yyqcd_nlo"):
        print("cptime")
        #s.system("cp successfu_pairs.py success_mass_pairs_f3c_yyqcd_nlo.py")
        shutil.copy("success_mass_pairs.py","success_mass_pairs_f3c_yyqcd_nlo.py")
    if(opt.model == "f3c_xx_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_f3c_xx_nlo.py")

        #f3v
    if(opt.model == "f3v_yyqcd_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_f3v_yyqcd_nlo.py")
    if(opt.model == "f3v_xx_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_f3v_xx_nlo.py")
        #f3w
    if(opt.model == "f3w_yyqcd_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_f3w_yyqcd_nlo.py")
    if(opt.model == "f3w_xx_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_f3w_xx_nlo.py")
        #f3s
    if(opt.model == "f3s_xx_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_f3s_xx_nlo.py")
    if(opt.model == "f3s_xx_lo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_f3s_xx_lo.py")

        #s3d
    if(opt.model == "s3d_yyqcd_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_s3d_yyqcd_nlo.py")
    if(opt.model == "s3d_xx_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_s3d_xx_nlo.py")

        #s3m
    if(opt.model == "s3m_yyqcd_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_s3m_yyqcd_nlo.py")
    if(opt.model == "s3m_xx_nlo"):
        shutil.copy("success_mass_pairs.py","success_mass_pairs_s3m_xx_nlo.py")
    
