
import sys
import os
import time
from glob import iglob
import shutil
import getopt

"""
class document:
    n_secions=0
    input_file=None
"""

def extract_block( input, start_string, end_string ):
    
    blocks= []
    
    for n1 in range(len(input)):
        if input[n1] != None and start_string in input[n1][1]:
            block = []
            for n2 in range(n1+1, len(input)):
                if end_string in input[n2][1]:
                    input[n2] = None
                    break
                else:
                    block.append(input[n2])
                    input[n2] = None
            input[n1] = None
            blocks.append(block)
    
    while None in input:
        input.remove(None)
    
    return blocks


def count_indents( line, indent=" "*4 ):
    # All characters in indent must be the same.
    c = indent[0]
    pos=0
    while pos<len(line):
        if line[pos] != c:
            break
        pos += 1
    line = line[pos:]
    return (line, pos/len(indent), pos%len(indent) )




def parse(input_file ):
    
    print "parsing..."
    
    # preprocessing...
    
    tab = " "*4
    
    lines = [ (line_number+1, line) for line_number, line in enumerate([ line for line in input_file ]) ] 
    
    blocks = extract_block( lines, start_string='\"\"\"', end_string='\"\"\"' )
    
    for ln, line in enumerate(lines):
        ( trimmed_line, level, remainder ) = count_indents( line[1], tab )
        if remainder != 0:
            print "error: bad indentation at line ", line[0]
            quit()
        lines[ln] = ( line[0], level, trimmed_line )
    
    ln = 0
    while ln < len(lines):
        if lines[ln][2] == '\n' or lines[ln][2] == '':
            lines.pop(ln)
        else:
            ln += 1
    
    lines = [ (line[0], line[1]-lines[0][1], line[2].replace('\n','') ) for line in lines ]
    
    for ln,line in enumerate(lines):
        if ln < len(lines)-1:
            diff = lines[ln+1][1]-lines[ln][1]
            if diff>1:
                print "error: unexpected indent, of the first kind, at line", line[0]+1
                quit()
    
    # Parsing in earnest...
    
    def is_keyword(token ):
        if token[-1] != ':':
            return False
        for c in token[0:len(token)-1]:
            if not c.isalpha():
                return False
        return True
    
    lines = [ (line[0], line[1], is_keyword(line[2]), line[2]) for line in lines ]
    
    """
    class branch:
        def __init__(self, type=None,tokens=[], level=None ):
            self.type = type
            self.tokens = tokens
            self.level = level
        
        def parse(self, lines ):
            
            pos=0
            for ln,line in enumerate(lines):
                if line[1] <= self.level:
                    break
                pos=ln
            print lines[pos][0]
   
    
    b = branch(level=0)
    b.parse(lines[1:])
     """
    
    #document = branch(type='keywords', level=0 )
    
    document = None
    
    """
    for ln,line in enumerate(lines):
        
        token = line[2]
        
        if is_keyword(token ):
            None
        else:
            None
    """
    
    """
    for ln,line in enumerate(lines):
        print line
    """
    
    return lines







def compile(lines, output, macro, preamble ):
    print "compiling..."
    
    out_file = open(output_fname, 'w')
    
    for line in preamble:
        out_file.write(line)
    
    for line in macro:
        out_file.write(line)
    
    out_file.write("\n\\begin{document}\n")
    
    pos=0
    while pos < len(lines):
        
        print lines[pos]
        
        pos += 1
    
    
    out_file.write("\n\\end{document}\n")
    out_file.close()



def parse_args(args, opts):
    
    values = [ [] for opt in opts ]
    flat_opts = []
    for opt in opts:
        if isinstance(opt,list):    
            flat_opts.extend(opt)
        else:
            flat_opts.append(opt)
    
    for arg_number, arg in enumerate(args):
        for opt_number, opt in enumerate(opts):
            if arg in opt and len(args) > arg_number+1 and args[arg_number+1] not in flat_opts:
                values[opt_number].append(args[arg_number+1])
    
    return values



if __name__ == "__main__":
    
    args = sys.argv[1:]
    
    [input_args, output_args, macro_args, preamble_args] = parse_args(args, [['-in','-i','-input','--input'], ['-out','-o','-output','--output'], ['-m','-macros','--macros'],['-p','-pa','-preamble','--preamble'] ] )
    
    input = input_fname = None
    output = output_fname = None
    macro = macro_fname = None
    preamble = preamble_fname = None
    
    if len(input_args) == 0:
        print "error: no input files understood."
        quit()
    
    try:
        if len(output_args) == 0:
            output_fname = 'out.tex'
        else:
            output_fname = output_args[0]
        output = open( output_fname, 'w' )
    except:
        print "error: couldn't open output file: ", output_fname
    
    try:
        if len(macro_args) == 0:
            macro_fname = 'std_macros.tex'
        else:
            macro_fname = macro_args[0]
        macro = open( macro_fname, 'r' )
    except:
        print "error: couldn't open macro file: ", macro_fname
    
    try:
        if len(preamble_args) == 0:
            preamble_fname = 'std_preamble.tex'
        else:
            preamble_fname = preamble_args[0]
        preamble = open( preamble_fname, 'r' )
    except:
        print "error: couldn't open preamble file: ", preamble_fname
    
    
    for input_fname in input_args:
        
        try:    
            input = open( input_fname, 'r' )
        except:
            print "error: couldn't open input file: ", input_fname
            quit()
        
        doc = parse(input)
        compile(doc, output, macro, preamble )
        input.close()
        
        """
        time.sleep(0.1)        
        os.system( "pdflatex " + output_fname )
        basename, extension = os.path.splitext(output_fname)
        os.system( "rm " + basename + '.log' )
        basename, extension = os.path.splitext(output_fname)
        os.system( "rm " + basename + '.aux' )
        
        """
