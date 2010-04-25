
import sys
import os
import time

from settings import *


class document:
    n_secions=0
    
    
    
def parse(file ):
    print "parsing..."
    doc = document()
    
    
    
    return doc


def compile(doc, output_fname, preamble=std_preamble, macros="" ):
    print "compiling..."
    
    out_file = open(output_fname, 'w')
    
    out_file.write(preamble)
    out_file.write(macros)
    out_file.write("\n\\begin{document}\n")
    
    out_file.write("afdlkngrangkrngfkrNG rtorngonrg \n rtreqt aretqret ateqtr4q")
    
    out_file.write("\n\\end{document}\n")
    out_file.close()
    time.sleep(0.0)
    
    os.system( "pdflatex " + output_fname )
    basename, extension = os.path.splitext(output_fname)
    os.system( "rm " + basename + '.log' )
    basename, extension = os.path.splitext(output_fname)
    os.system( "rm " + basename + '.aux' )



if __name__ == "__main__":
    
    args = []
    for arg in sys.argv:
        if arg != "pyMathNotes.py":
            args.append(arg)
    
    files = []
    for arg_number, arg in enumerate(args):
        try:
            file = open(arg)
            out_fname = ""
            if '.' in arg:
                basename, extension = os.path.splitext(arg)
                out_fname = basename + '.tex'
            else:
                out_fname = arg + '.tex'
            files.append( (file, out_fname) )
        except:
            print "arguement ", arg_number+1, " not understood."
    
    for (file, out_fname) in files:
        doc = parse(file)
        compile(doc, out_fname)
        file.close()
    
