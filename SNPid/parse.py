import cPickle as pickle

inputfile  = "data.bed"
CHRCOL = 0
BPCOL  = 2
RSCOL  = 3

with open(inputfile,"r") as fin:
    bpgen = ("{}:{}".format(s[CHRCOL][3:],s[BPCOL]) for s in (line.split() for line in fin))
    bpselection2M = frozenset(bpgen)
    pickle.dump(bpselection2M, open("snpid.pickle","wb"))
