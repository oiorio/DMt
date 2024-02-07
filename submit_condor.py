import os
import optparse
import sys
import fileinput
import time

usage = 'python submit_condor.py -r runmg.mg  -g runmg_generata.mg -O local_directory -o eos_directory' 
parser = optparse.OptionParser(usage)
parser.add_option('-m', '--mode', dest='mode', type=str, default = '', help='Enter mode: G = Generate, M = Madanalysis, default = GM' )
parser.add_option('-r', '--runmg', dest='runmg', type=str, default = '', help='Please enter conf file')
parser.add_option('-g', '--runmg_generate', dest='runmg_generate', type=str, default = '', help='Please enter generation file')
parser.add_option('-R', '--runmg_recast', dest='runmg_recast', type=str, default = '', help='Please enter recast file')
parser.add_option('-S', '--runmg_sfs', dest='runmg_sfs', type=str, default = '', help='Please enter sfs file')
parser.add_option('-l', '--label', dest='job_label', type=str, default = 'job0', help='Please enter job label')
parser.add_option('-O', dest='output_file',type=str,default='',help='madgraph output directory')
parser.add_option('-o','--output', dest='out_store_dir',type=str,default='/eos/home-o/oiorio/DMMC/XSecs',help='file storage directory')
parser.add_option('--dryrun', dest='dryrun', default = False, action='store_true', help="dryrun")
(opt, args) = parser.parse_args()
#Insert here your uid... you can see it typing echo $uid

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
if username == 'adeiorio':
    uid = 103214
elif username == 'acagnott':
    uid = 140541
elif username == 'oiorio':
    uid = 31365

mode=opt.mode

def sub_writer(label,work_dir="./",basedir="./",runner_dir="./"):
    f = open(runner_dir+"/condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    #f.write('requirements = (TARGET.OpSysAndVer =?= "CentOS7") && Request_Disk >= 25000000\n')
    #f.write('requirements = (TARGET.OpSysAndVer =?= "CentOS7") \n')
    f.write('MY.WantOS               = "el7" \n')
    
    #    f.write('requirements = (TARGET.OpSysAndVer =?= "AlmaLinux9") \n')
    f.write("+JobFlavour             = \"testmatch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch\ = 3 days, nextweek     = 1 week
    #f.write("+JobFlavour             = \"microcentury\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch\ = 3 days, nextweek     = 1 week
    f.write("executable              = "+runner_dir+"/runner.sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = "+basedir+"/condor/output/"+ label+".out\n")
    f.write("error                   = "+basedir+"/condor/error/"+ label+".err\n")
    f.write("log                     = "+basedir+"/condor/log/"+ label+".log\n")

    f.write("queue\n")

def editrecastfile(summary,recast_file):
    xsec = "1" 
    if(not os.path.exists(summary)):
        print("summary does not exist! Not changing the xsec")
    else:    
        with open(summary, "r") as fin:
            flines = fin.readlines()
            lxsec=""
            for line in flines:
                if "Total cross section" in line:
                    lxsec= line
            xsec=lxsec.split()[3]
            print("xsec found is ",xsec)

    print("recast exists? " ,os.path.exists(recast_file))
    if(not os.path.exists(recast_file)):
        print("recast file does not exist! Doing nothing")
        return
    
    #xsec=1.
    with open(recast_file+"fix",'w') as fo:
        stringrec=""
        with open(recast_file,"r") as f2:#, 
            #print("reading of the file ",f2.read())
            f2.seek(0)
            rlines = f2.readlines()
            for li in rlines:
                stringrec=stringrec+li.replace(".xsection = 1",".xsection = "+str(xsec)+"")
                #print(stringrec)
            f2.close()
        fo.write(stringrec)
        fo.close()

def runner_writer(conf_file, gen_file,output_file,out_store_dir,
                  mgdir="/afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15",
                  recast_file=None,sfs_file=None,xsec_file_format="parton_systematics",pyenvdir="py3_env2",recast_dir="/afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/MA5/",
                  runner_dir=".",work_dir=".", out_eosdir=".", mode= mode, useMadSTR=False):
    os.system("rm "+runner_dir+"/runner.sh")
    f = open(runner_dir+"/runner.sh", "w")
    #    if not os.path.exists(work_dir):
        #os.system("cp -r "+out_eosdir + " "+ work_dir)
        #f.write("cmssw-el7")
    f.write("#!/usr/bin/bash \n")
    f.write("bash \n")
    f.write("source "+mgdir+"/dmmc.sh \n")
    f.write("echo $LD_LIBRARY_PATH \n" )
    f.write("echo $PYTHONPATH \n" )
    f.write("mkdir -p " + work_dir + "\n")
    if not os.path.exists(out_eosdir):
        f.write("mkdir -p " + out_eosdir + "\n")
    f.write("cd "+work_dir +" \n")
    if "G" in mode:
        if not(useMadSTR):
            f.write("python2.7 "+mgdir+"/bin/mg5_aMC "+mgdir+"/"+conf_file+"\n")
            f.write("sleep 5 \n")
            if ("_NLO_" in gen_file):
                f.write("python2.7 "+mgdir+"/bin/mg5_aMC "+mgdir+"/"+gen_file+"\n")
            if ("_LO_" in gen_file):
                f.write("python2.7 "+mgdir+"/bin/mg5_aMC < "+mgdir+"/"+gen_file+"\n")
            f.write("sleep 5 \n")
        else:
            f.write("python2.7 "+mgdir+"/bin/mg5_aMC --mode=MadSTR "+mgdir+"/"+conf_file+"\n")
            f.write("sleep 5 \n")
            f.write("cd "+workdir+"\n")
            f.write("cp "+workdir+"/bin/mg5_aMC "+mgdir+"/"+gen_file+" . \n")
            f.write("python2.7 "+workdir+"/bin/aMCatNLO "+gen_file+"\n")
            f.write("sleep 5 \n")
    f.write("source /cvmfs/sw.hsf.org/spackages7/key4hep-stack/2023-04-08/x86_64-centos7-gcc11.2.0-opt/urwcv/setup.sh \n")
    if (not (recast_file is None) and "M" in mode):
        if not recast_file=='':
            #f.write("source "+mgdir+"/"+pyenvdir+"/bin/activate \n")
            f.write("cd "+mgdir +" \n")
            recastform=""
            if(xsec_file_format=="summary"):
                recastform="/summary.txt -f "+xsec_file_format+" \n "
            if(xsec_file_format=="parton_systematics"):
                recastform="/parton_systematics.log -f "+xsec_file_format+" \n "
                
            f.write("python "+mgdir+"/editrecastfile.py -r ./"+recast_file+ " -s "+work_dir+"/"+output_file+"/Events/run_01/"+recastform)
            f.write("python "+mgdir+"/editrecastfile.py -r ./"+sfs_file+ " -s "+work_dir+"/"+output_file+"/Events/run_01/"+recastform)
            f.write("cd " + work_dir +"\n")            
            #old ideas
            #editrecastfile(summary=work_dir+"/"+output_file+"/Events/run_01/summary.txt",recast_file="./"+recast_file)
            #            f.write('bash \n')
            #f.write("alias alias python=")
            #f.write("rm ANALYSIS* madanalysis5 -rf \n")
            #f.write("rm py3_env -rf \n")
            #create the pyenv locally
            #f.write("python3 -m venv py3_env3 \n")

            
            pyenv_dir="/afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/py3_env3/bin/"
            f.write("source "+pyenv_dir+"/activate \n")
            
            #pyenv_dir = work_dir+"/py3_env3/bin/"
            #madandir=mgdir+"/madanalysis5"
            madandir=work_dir#+"/madanalysis5"
            #madandir = "/tmp/oiorio/"
            f.write("echo $SCRAM_ARCH \n")
            #f.write("source /cvmfs/sft.cern.ch/lcg/contrib/gcc/13/x86_64-centos7/setup.sh \n")
            #f.write("source /cvmfs/sft.cern.ch/lcg/contrib/gcc/11.2.0/x86_64-centos7/setup.sh \n")
            #f.write("source /cvmfs/sft.cern.ch/lcg/external/gcc/4.8.1/x86_64-centos7/setup.sh \n")
            #echo $SCRAM_ARCH
            #f.write('git clone https://github.com/MadAnalysis/madanalysis5.git madanalysis5 \n')
            f.write("cd "+madandir+" \n")
            f.write("rm madanalysis5 -rf \n")
            f.write('git clone https://github.com/MadAnalysis/madanalysis5.git -b v1.10.10 madanalysis5 \n')
            f.write('cp '+mgdir+'/install_zlib_fix.py '+madandir+'/madanalysis5/madanalysis/install/install_zlib.py \n')
            f.write('cd '+madandir+'/madanalysis5 \n')
            #f.write('cd madanalysis5 \n') #If
            f.write('mkdir -p tools/PADForSFS \n')
            f.write('chmod a+xr tools/PADForSFS \n')
            
            #pyenv version1
            #f.write(pyenv_dir+'pip3 install -r '+recast_dir+"../madanalysis5/requirements.txt \n")
            #f.write(pyenv_dir+'pip3 install --upgrade pip \n ')
            #f.write("gcc --version \n")
            #f.write("source "+mgdir+"/dmmc_madanalysis.sh \n")
            #f.write(pyenv_dir+"/python3 "+recast_dir+"../madanalysis5/bin/ma5 -s "+recast_dir+"/MA5AuxiliaryFiles/MA5_installpackages \n")
            #f.write(pyenv_dir+"/python3 "+recast_dir+"/madanalysis5/bin/ma5 -R -s "+mgdir+"/"+recast_file+"fix \n")
            
            #pyenv version2
            f.write("pwd \n")
            #f.write(pyenv_dir+'/pip3 install --upgrade pip \n')
            #f.write(pyenv_dir+'/pip3 install -r requirements.txt \n')
            f.write("gcc --version \n")
            #            f.write("source "+mgdir+"/dmmc_madanalysis.sh \n")
            
            #Installing the madanalysis in the work directory ####
            installmadan=False
            installmadan=True
            if(installmadan):
                #madandir=work_dir+"/madanalysis5"
                #madandir=
                #root attempts
                f.write("source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.08/x86_64-centos7-gcc48-opt/bin/thisroot.sh \n")
                
                print("installed at  ",madandir)
                f.write("LD_LIBRARY_PATH=/afs/cern.ch/work/o/oiorio/DMMC/LHAPDFInstall/lib:$LD_LIBRARY_PATH \n")
                f.write("LD_LIBRARY_PATH="+madandir+"/madanalysis5/tools/SampleAnalyzer/Lib:$LD_LIBRARY_PATH \n")
                f.write("LD_LIBRARY_PATH="+madandir+"/madanalysis5/tools/SampleAnalyzer/ExternalSymLink/Lib:$LD_LIBRARY_PATH \n")
                f.write("LD_LIBRARY_PATH="+madandir+"/madanalysis5/tools/delphes:$LD_LIBRARY_PATH \n")
                f.write("export LD_LIBRARY_PATH \n")
                #f.write("PYTHONPATH=/afs/cern.ch/work/o/oiorio/DMMC/LHAPDFInstall/lib/python2.7")
                #export PYTHONPATH
                f.write("ROOT_INCLUDE_PATH="+madandir+"/MA5/madanalysis5/tools/delphes/external:$ROOT_INCLUDE_PATH \n")
                f.write("ROOT_INCLUDE_PATH="+madandir+"/madanalysis5/tools/delphes/external:$ROOT_INCLUDE_PATH \n")
                f.write("export ROOT_INCLUDE_PATH \n")


                pycommand="python "
                usepyenv=False
                if(usepyenv):
                    pycommand=pyenv_dir+"/python3 "
                
                f.write(pycommand+madandir+"/madanalysis5/bin/ma5 -s "+recast_dir+"/MA5AuxiliaryFiles/MA5_installpackages_nondelphes \n")       
                f.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/setup.sh \n")
                f.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/bin/thisroot.sh \n")

                f.write(pycommand+madandir+"/madanalysis5/bin/ma5 -s "+recast_dir+"/MA5AuxiliaryFiles/MA5_installpackages_delphes \n")
                f.write(pycommand+madandir+"/madanalysis5/bin/ma5 -s "+recast_dir+"/MA5AuxiliaryFiles/MA5_installpackages_pad_only \n")

                f.write("cp "+recast_dir+"/MA5AuxiliaryFiles/run_recast.py "+madandir+"/madanalysis5/madanalysis/misc/ \n")
                f.write("cp "+recast_dir+"/MA5AuxiliaryFiles/recast_configuration.py "+madandir+"/madanalysis5/madanalysis/configuration/ \n")

                f.write("cp "+mgdir+"/RecastingCards/delphes* "+madandir+"/madanalysis5/tools/PAD/Input/Cards/ \n")
                f.write("cp "+mgdir+"/RecastingCards/sfs* "+madandir+"/madanalysis5/tools/PADForSFS/Input/Cards/ \n")

                f.write("cp /afs/cern.ch/user/o/oiorio/public/DMMC/atlas_susy_2018_32.info "+madandir+"/madanalysis5/tools/PAD/Build/SampleAnalyzer/User/Analyzer/ \n")
                f.write("mv "+madandir+"/madanalysis5/tools/PAD/Build/SampleAnalyzer/User/Analyzer/atlas_susy_2018_32_all.json "+madandir+"/madanalysis5/tools/PAD/Build/SampleAnalyzer/User/Analyzer/atlas_susy_2018_32.json \n")
                
            #ENDInstalling the madanalysis in the work directory 

            f.write("pwd \n")



            f.write("cp "+mgdir+"/"+recast_file+"fix . \n")
            f.write("cp "+mgdir+"/"+sfs_file+"fix . \n")

            f.write(pycommand+madandir+"/madanalysis5/bin/ma5 -R -s ./"+recast_file+"fix \n")
            #f.write("cp -r "+madandir+"/madanalysis5/ANALYSIS_0 "+work_dir+"_ANALYSIS_0 \n")
            f.write("rm -rf "+madandir+"ANALYSIS_0_RecastRun/Output/SAF/*/RecoEvents* \n")
            f.write("cp -rf "+madandir+"/madanalysis5/ANALYSIS_0 "+out_eosdir+"_ANALYSIS_0 \n")

            

            ###
            f.write("cp -rf " + work_dir+"/"+output_file+"/Events/run_01/events.lhe.gz " + out_eosdir+"/ \n")
            f.write("cp -rf " + work_dir+"/"+output_file+"/Events/run_01/unweighted_events.lhe.gz " + out_eosdir+"/ \n")
            f.write("cp -rf " + work_dir+"/"+output_file+"/Events/run_01_decayed_1/events.lhe.gz " + out_eosdir+"/events_decayed_1.lhe.gz \n")

            ###
            f.write("cp -rf " + work_dir+"/"+output_file+"/Events/run_01/summary.txt " + out_eosdir+"/ \n")
            f.write("cp -rf " + work_dir+"/"+output_file+"/Events/run_01/parton_systematics.log " + out_eosdir+"/ \n")
            f.write("cp -rf " + work_dir+"/"+output_file+"/Events/run_01_decayed_01/run_01_decayed_1_tag_1_banner.txt " + out_eosdir+"/ \n")


            
            #f.write("cp -r " + work_dir+"/"+output_file+"/Events/run_01/summary.txt" + out_eosdir+"/")
            f.write(pycommand+madandir+"/madanalysis5/bin/ma5 -s ./"+sfs_file+"fix \n")

            f.write("rm -rf "+madandir+"/madanalysis5/ANALYSIS_1/Output/SAF/*/lheEvents0_0/ma5_events.lhe* \n")
            f.write("cp -rf "+madandir+"/madanalysis5/ANALYSIS_1 "+out_eosdir+"_ANALYSIS_1 \n")

            
            f.write("cd "+work_dir+" \n")
            f.write(pycommand+mgdir+"/cleardir.py -d ./ -f "+output_file +" -p 'DMtsimp/MG5Runs/' \n")
            if (work_dir != out_eosdir) and not (out_eosdir is None):
                f.write("sleep 10 \n") #wait a few seconds to make sure to not remove anything important
                f.write("rm -rf "+ work_dir+" \n")
            f.close()

    pycommand="python "
    fcl = open(runner_dir+"/cleaner.sh", "w")
    fcl.write("cd "+work_dir+" \n")
    fcl.write(pycommand+mgdir+"/cleardir.py -F -d ./ -f "+output_file +" -p 'DMtsimp/MG5Runs/' \n")
    fcl.write("cd - \n")
    print("fcl is ", fcl)
    fcl.close()

                #f.write(pyenv_dir+"/python3 "+madandir+"/bin/ma5 -R -s ./"+recast_file+"fix \n")

            
            #f.write(pyenv_dir+"/python "+recast_dir+"/madanalysis5/bin/ma5 -R -s "+mgdir+"/"+recast_file+"fix \n")
        
        # if(out_store_dir != ''):
        # f.write("mv "+output_file+" "+out_store_dir +" \n")


label = opt.job_label
conf_file = opt.runmg
gen_file = opt.runmg_generate
recast_file = opt.runmg_recast
sfs_file = opt.runmg_sfs
dryrun = opt.dryrun
output_file = opt.output_file
out_store_dir = opt.out_store_dir 

basedir="/afs/cern.ch/work/o/oiorio/DMMC/MG5_aMC_v2_9_15/"
runner_dir=basedir+"/condor/work/"+label

#runner_dir

eosdir="/tmp/mjf-oiorio/"
outeosdir="/eos/home-o/oiorio/DMMC/Events/"
work_dir=eosdir+"/condor/work/"+label
out_eosdir=outeosdir+"/condor/work/"+label
#work_dir=basedir+"/condor/work/"+label#make local work directory 

if not os.path.exists(outeosdir+"condor/work"):
    os.makedirs(outeosdir+"condor/work")
if not os.path.exists(basedir+"condor/work"):
    os.makedirs(basedir+"condor/work")
if not os.path.exists(outeosdir+"condor/work/"+label):
    os.makedirs(outeosdir+"condor/work/"+label)

if not os.path.exists(basedir+"condor/work/"+label):
    os.makedirs(basedir+"condor/work/"+label)
if not os.path.exists("condor/output"):
    os.makedirs("condor/output")
if not os.path.exists("condor/error"):
    os.makedirs("condor/error")
if not os.path.exists("condor/log"):
    os.makedirs("condor/log")
if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

print("submitting job ...")
print("job label = ", label)
print("run instruction file =", conf_file)
print("topology instruction file =", gen_file)
print("output file =", output_file)
print("output store directory =", out_store_dir)
print("work directory =", work_dir)
runner_writer(conf_file, gen_file,output_file,out_store_dir,runner_dir=runner_dir,work_dir=work_dir,recast_file=recast_file,sfs_file=sfs_file,out_eosdir=out_eosdir)
print("runner.sh file, DONE!")
sub_writer(label,work_dir=work_dir,basedir=basedir,runner_dir=runner_dir)
#time.sleep(10)
#os.system("cd "+work_dir)
print("condor.sub file, DONE!")
if not dryrun: 
    if(mode =="C"):
        print()
        os.system('source '+runner_dir+'/cleaner.sh &')
    else:
        print()
        os.popen('condor_submit '+runner_dir+'/condor.sub')
    
#os.system("cd -")
print("DONE!")
