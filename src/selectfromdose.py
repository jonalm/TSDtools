from __future__ import print_function
from os.path import isfile
import numpy as np
import argparse
import datetime
import gzip
import os.path

def logprint(msg, logfilename):
    with open(logfilename, "a+") as fout:
        print(msg, file=fout)
        print(msg)

def load_set(filename):
    with open(filename, "r") as fin:
        return {line.split("\n")[0] for line in fin}

def col_selection(sheader, subjectselection):
    ## returns logical array indicating the position of the selected subjects
    # and a set of the found subjects
    res = np.zeros(len(sheader), dtype=np.bool)
    res[:3] = 1 # SNP, A1, A2
    found = set()
    for i, sh in enumerate(sheader):
        subject = sh.split(" ")[0]
        if subject in subjectselection:
            res[i] = 1
            found.add(subject)
    return res, found

if __name__ == "__main__":
    # parse script input
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="<file name>", type=str, nargs="+",
                        help="action done on each filename")
    parser.add_argument('-snp', '--snpids', required=True,
                        help=("text file containing the selected SNPid "
                              "on the form 'chrnumber:basepairnumber\n' "
                              "consisten width dose file"))
    parser.add_argument('-sub', '--subjects', required=True,
                        help=("text file containing the selected subjecs "
                              "on the form 'subjectid\n' "
                              "consistend with dose file"))
    parser.add_argument('-o', '--out_dir',  required=True,
                        help="directory where output is stored")
    parser.add_argument("-v", "--verbosity", action="store_true",
                        help="increase output verbosity")
    args = parser.parse_args()

    print() #newline
    logfn = os.path.join(args.out_dir, "log.txt")
    with open(logfn, "w`") as f:
        f.write("\nlog started {}\n\n".format(datetime.datetime.now()))

    logprint("file input {}".format(args.files), logfn)

    # make compatible with gz files
    if all(f[-2:]=="gz" for f in args.files):
        logprint("assume gzipped input", logfn)
        gzcompatible_open = gzip.open
    elif all(f[-4:]=="dose" for f in args.files):
        logprint("assume plain text input", logfn)
        gzcompatible_open = open
    else:
        raise Exception("Either all or none of file name inputs need to end with 'gz'")

    selected_SNP = load_set(args.snpids)
    selected_subjects = load_set(args.subjects)

    logprint("", logfn)
    logprint("{}\tcandidate SNPid in file    : {}".format(len(selected_SNP), args.snpids), logfn)
    logprint("{}\tcandidate subjects in file : {}".format(len(selected_subjects), args.subjects), logfn)

    for finame in args.files:
        foname = os.path.join(args.out_dir, "subset_{}".format(os.path.basename(finame)))

        with gzcompatible_open(finame,"r") as fi, gzcompatible_open(foname,"w") as fo:
            snp_in_fi = set()
            written_lines = 0

            header = fi.next()
            sheader = np.array(header.split("\t"))
            col_sv, subjects_in_fi = col_selection(sheader, selected_subjects)
            fo.write("\t".join(sheader[col_sv]))

            for line in fi:
                split = line.find("\t")
                snp = line[:split]
                if snp in selected_SNP:
                    sline = np.array(line.split("\t"))
                    fo.write("\t".join(sline[col_sv]))
                    snp_in_fi.add(snp)
                    written_lines += 1

        logprint("\nin file \t{}:".format(finame), logfn)
        logprint("write to\t{}:".format(foname), logfn)
        logprint("found {} snps".format(len(snp_in_fi)), logfn)
        logprint("wrote {} lines".format(written_lines), logfn)
        logprint("found {} subjects".format(len(subjects_in_fi)), logfn)
