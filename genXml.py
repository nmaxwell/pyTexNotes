
import sys
import os
import tools


# formatting things and parameters:

TAB = " "*4
XML_TAB = ' '*4
EXTENSION = '.xml'

def is_keyword(token ):
        if token[-1] != ':':
            return False
        for c in token[0:len(token)-1]:
            if not c.isalpha() and c not in [',', '_' ]:
                return False
        return True


# code:


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




# main part of the code:

def to_xml(input_file ):
    sys.stdout.write("Parsing and compiling to xml...\t")
    
    # preprocessing

    lines = [ (line_number+1, line) for line_number, line in enumerate([ line for line in input_file ]) ] 
    
    if len(lines) == 0:
        print "\nEmpty file."
        return ([], [])
    
    blocks = extract_block( lines, start_string='\"\"\"', end_string='\"\"\"' )
    
    for ln, line in enumerate(lines):
        ( trimmed_line, level, remainder ) = count_indents( line[1], TAB )
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
    
    # checking indentations
    
    for ln,line in enumerate(lines):
        if ln < len(lines)-1:
            diff = lines[ln+1][1]-lines[ln][1]
            if diff>1:
                print "error: unexpected indent, of the first kind, at line", line[0]+1
                quit()
    
    # get difference in indentation between this line and next
    
    new_lines=[(lines[0][0], lines[0][1], 0, lines[0][2])]
    for ln,line in enumerate(lines[1:]):
        new_lines.append((line[0], line[1], line[1]-new_lines[-1][1], line[2]))
    lines=new_lines
    
    # expand comma delimeted keywords into seperate, nested keywords
    
    new_lines=[]
    indent=0
    for line in lines:
        if is_keyword(line[3]):
            if ',' in line[3]:
                if line[2] > 0:
                    indent += 1
                if line[2] <0:
                    indent = line[1]
                for k,x in enumerate(line[3].strip(':').split(',')):
                    if len(x)<1:
                        print "error: empty keyword at line", line[0]
                        quit()
                    new_lines.append((line[0], indent, x+':'))
                    indent+=1
                indent+=-1
            else:
                if line[2] > 0:
                    indent += 1
                if line[2] <0:
                    indent = line[1]
                new_lines.append((line[0], indent, line[3]))
        else:
            if line[2] > 0:
                indent += 1
            if line[2] <0:
                indent = line[1]
            new_lines.append((line[0], indent, line[3]))
    lines=new_lines
    
    """
    print '\n'*4
    for line in lines:
        print line
    print '\n'*4
    """
    
    #generate xml lines
    
    xml_lines = ["<?xml version=\"1.0\"?>\n"]
    xml_line_numbers = [None]
    
    queue=[]
    indent=0
    for ln,line in enumerate(lines):
    
        while line[1] < indent:
            indent += -1
            xml_lines.append( XML_TAB*indent + '</' + queue.pop() + '>' )
            xml_line_numbers.append(None)
    
        if is_keyword(line[2]):
            name = line[2].strip(':')
                
            xml_lines.append( XML_TAB*indent + '<' + name + '>' )
            indent += 1
            xml_line_numbers.append(line[0])
            queue.append(name)
        else:
            if indent == line[1]:
                xml_lines.append( XML_TAB*indent + line[2] )
                xml_line_numbers.append(line[0])
    
    while len(queue)>0:
        indent += -1
        xml_lines.append( XML_TAB*(indent) + '</' + queue.pop() + '>' )
        xml_line_numbers.append(None)
    
    sys.stdout.write('done.\n')
    return xml_lines, xml_line_numbers




if __name__ == "__main__":
    
    args = sys.argv[1:]
    
    [input_args, output_args ] = tools.parse_args(args, [['-in','-i','-input','--input'], ['-out','-o','-output','--output'] ] )
    
    input = input_fname = None
    output = output_fname = None
    
    if len(input_args) == 0:
        print "error: no input files understood."
        quit()
    
    while len(output_args) < len(input_args):
        output_args.append('')
    
    for k,ofname in enumerate(output_args):
        if ofname in [ '', None ]:
            ifname = input_args[k]
            (name, blah) = os.path.splitext(ifname)
            output_args[k] = name + EXTENSION
    
    
    for num in range(len(input_args)):
    
        input_fname = input_args[k]
        output_fname = output_args[k]
        
        try:
            input = open( input_fname, 'r' )
        except:
            print "error: couldn't open input file: ", input_fname
            quit()
        
        try:
            output = open( output_fname, 'w' )
        except:
            print "error: couldn't open output file: ", output_fname
            quit()
        
        xml_lines, xml_line_numbers = to_xml(input)
        
        for line in xml_lines:
            output.write(line + "\n" )
        
        output.close()
        input.close()
        





