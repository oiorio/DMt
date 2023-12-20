import os
import optparse
import sys
import fileinput

usage = 'python cleardir.py -d directory -f filename'
parser = optparse.OptionParser(usage)
parser.add_option('-s', '--summaryfile', dest='summary', type=str, default = '', help='Summary file name')
parser.add_option('-r', '--recastfile', dest='recast', type=str, default = '', help='Recast file name')
parser.add_option('-n','--dryrun', dest='dryrun', default = False, action='store_true', help="dryrun")
parser.add_option('-f', '--fileformat', dest='fileformat', type=str, default = 'summary', help='Summary file format')
(opt, args) = parser.parse_args()

summary=opt.summary
recast=opt.recast
fileformat=opt.fileformat

def editrecastfile(summary=summary,recast_file=recast, fileformat=fileformat):
    xsec = "1" 
    if(not os.path.exists(summary)):
        print("summary does not exist! Not changing the xsec")
    else:    
        if(fileformat=="summary"):
            with open(summary, "r") as fin:
                flines = fin.readlines()
                lxsec=""
                for line in flines:
                    if "Total cross section" in line:
                        lxsec= line
                        xsec=lxsec.split()[3]
                print("xsec found is ",xsec)
        if (fileformat== "html"):
            print("html parsing not implemented yet!")

        if(fileformat=='parton_systematics'):
            with open(summary, "r") as fin:
                flines = fin.readlines()
                lxsec=""
                for line in flines:
                    if "original cross-section" in line:
                        lxsec= line
                        xsec=lxsec.split()[-1]
                        print("xsec found is ",xsec)


    print("recast exists? " ,os.path.exists(recast_file))
    if(not os.path.exists(recast_file)):
        print("recast file does not exist! Doing nothing")
        return
    
    #xsec=1.

    if not opt.dryrun:
        with open(recast_file+"fix",'w') as fo:
       
            stringrec=""
            with open(recast_file,"r") as f2:#, 
                #print("reading of the file ",f2.read())
                f2.seek(0)
                rlines = f2.readlines()
                for li in rlines:
                    stringrec=stringrec+li.replace(".xsection = 1",".xsection = "+str(xsec)+"").replace(".xsection = SED_CROSSSECTION",".xsection = "+str(xsec)+"")
                    #print(stringrec)
                f2.close()
            fo.write(stringrec)
            fo.close()


editrecastfile()
