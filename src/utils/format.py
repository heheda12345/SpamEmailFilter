import sys
import re
if __name__ == '__main__':
    f = open(sys.argv[1])
    st = f.read()
    f.close()
    st = re.sub('\033\[\d*(;\d*)*m', "", st)
    f = open(sys.argv[1], "w")
    f.write(st)
    f.close()