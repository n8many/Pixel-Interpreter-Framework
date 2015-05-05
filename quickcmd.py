from interp import Interp
import sys,getopt
def main(argv):
    try:
        opts, args = getopt.getopt(argv,'c:')
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-c':
            print arg
            Interp(arg)
        else:
            print opt    


if __name__ == "__main__":
    main(sys.argv[1:])
