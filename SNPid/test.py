import cPickle as pickle

total = set()

for i in range(1,23):
    bp = pickle.load(open("2M/chr{}_basepairs.pickle".format(i),"rb"))
    total.update(bp)
