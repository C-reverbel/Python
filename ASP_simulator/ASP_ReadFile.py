import sys, getopt

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'usage: ASP_ReadFile YourCircuitScript'
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print 'usage: ASP_ReadFile YourCircuitScript'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is: ', inputfile
   
   with open("Circ1.txt") as f:
      lines = f.readlines()
   print lines

if __name__ == "__main__":
   main(sys.argv[1:])