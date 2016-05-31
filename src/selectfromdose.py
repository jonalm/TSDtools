from os.path import isfile
import cPickle as pickle
import argparse
import gzip

# parse script input
parser = argparse.ArgumentParser()
parser.add_argument("files", metavar="<file name>", type=str, nargs="+",
                    help="action done on each filename")
parser.add_argument("-v", "--verbosity", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-d", "--verbosity", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()

if all(f[-2:]== "gz" for f in args.files):
    if args.verbosity:
        print "assume gzipped input", args.files
    open = gzip.open
    GZIP = True
elif not any(f[-4:]== "do" for f in args.files):
    if args.verbosity:
        print "assume plain text input", args.files
    GZIP = False    
else:
    raise Exception("Either all or none of file name inputs need to end with 'gz'")

for fn in args.files:
    with open(fn) as f:
        print f.next()
