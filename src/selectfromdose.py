from os.path import isfile
from itertools import compress
import cPickle as pickle
import numpy as np
import gzip
import os.path
from getcontrolID import getcontrolID

def load_bpset(chrnum, snpid_dir):
    try:
        filename = os.path.join(snpid_dir, "chr{}_basepairs.pickle".format(chrnum))
        bp = pickle.load(open(filename, "rb"))
        return bp
    except IOError:
        print "Couldn't find SNPid pickle file for chromosome {}".format(chrnum)
        raise

def col_selection(sheader, selectionset):
    res = np.zeros(len(sheader), dtype=np.bool)
    res[:3] = 1 # SNP, A1, A2

    for i, sh in enumerate(sheader):
        if sh.split(" ")[0] in selectionset:
            res[i] = 1

    return res

if __name__ == "__main__":
    # parse script input
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="<file name>", type=str, nargs="+",
                        help="action done on each filename")
    parser.add_argument('-i', '--snpid_dir', required=True,
                        help="directory where 'chrX_basepairs.pickle' are stored")
    parser.add_argument('-o', '--out_dir', default=".",
                        help="directory where output is stored")
    parser.add_argument("-v", "--verbosity", action="store_true",
                        help="increase output verbosity")
    args = parser.parse_args()

    ## selected individua
    selected_individuals = getcontrolID()

    if all(f[-2:]=="gz" for f in args.files):
        if args.verbosity:
            print "assume gzipped input", args.files
        fileopen = gzip.open
        GZIP = True
    elif all(f[-4:]=="dose" for f in args.files):
        if args.verbosity:
            print "assume plain text input", args.files
        fileopen = open
        GZIP = False
    else:
        raise Exception("Either all or none of file name inputs need to end with 'gz'")

    idCHRNUM = None
    for finame in args.files:
        foname = os.path.join(args.out_dir, "subset_{}".format(os.path.basename(finame)))


        with fileopen(finame,"r") as fi, fileopen(foname,"w") as fo:
            header = fi.next()
            sheader = np.array(header.split("\t"))
            col_sv = col_selection(sheader, selected_individuals)

            fo.write("\t".join(sheader[col_sv]))

            for line in fi:
                split = line.find(":")
                idend = line.find("\t")

                try:
                     lineCHRNUM = int(line[:split])
                except:
                     continue # chr not a number
                try:
                    lineBP = int(line[split+1:idend])
                except:
                    continue # no simple basepair

                if idCHRNUM != lineCHRNUM:
                    idCHRNUM = lineCHRNUM
                    bpset = load_bpset(idCHRNUM,args.snpid_dir)

                if lineBP in bpset:
                    sline = np.array(line.split("\t"))
                    fo.write("\t".join(sline[col_sv]))
else:
    pass
