import cPickle as pickle

inputfile  = "raw/2M/data.bed"
CHRCOL = 0
BPCOL  = 2
RSCOL  = 3

def baseparirselect(chrnum, lines):
    return (int(s[BPCOL]) for s in (line.split() for line in lines) if s[CHRCOL][3:]==str(chrnum))

for chrnum in range(1,23):
    with open(inputfile,"r") as fin:
        bp = frozenset(baseparirselect(chrnum, fin))
        pickle.dump(bp, open("chr{}_basepairs.pickle".format(chrnum),"wb"))
