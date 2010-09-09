
import sys
import os
#import xml.parsers.expat
from xml.dom import minidom
import unittest
import StringIO
import tools, toolbox


default_preamble = "/workspace/pyTexNotes/default_preamble.tex"
default_macros = "/workspace/pyTexNotes/default_macros.tex"

class to_tex:
    
    def __init__(self, input, asfile=True, aslines=False):
        asfile = not aslines
        
        #parse input
        if asfile is True:
            sock = toolbox.openAnything(input) 
            self.xmldoc = minidom.parse(sock).documentElement
            sock.close()
        elif aslines is True:
            
            inp = StringIO.StringIO("\n".join(input))
            self.xmldoc = minidom.parse(inp)
    
    def refresh(self, ):
        self.tex_lines = []
    
    def process(self, ):
        self.refresh()
        self.parse(self.xmldoc)
        return self.tex_lines
    
    
    def parse(self, node):

        if node is None:
            return None
        
        """parse a single XML node
        
        A parsed XML document (from minidom.parse) is a tree of nodes
        of various types.  Each node is represented by an instance of the
        corresponding Python class (Element for a tag, Text for
        text data, Document for the top-level document).  The following
        statement constructs the name of a class method based on the type
        of node we're parsing ("parse_Element" for an Element node,
        "parse_Text" for a Text node, etc.) and then calls the method.
        """
        parseMethod = getattr(self, "parse_%s" % node.__class__.__name__)
        parseMethod(node)
    
    def parse_Document(self, node):
        """parse the document node
        
        The document node by itself isn't interesting (to us), but
        its only child, node.documentElement, is: it's the root node
        of the grammar.
        """
        self.parse(node.documentElement)
        
    def parse_Text(self, node):
        
        text = node.data
        #print [ord(c) for c in text]
        #print [ord(c) for c in "\n    "]
        self.tex_lines.append(text)
        
    
    def parse_Element(self, node):
        """parse an element
        
        An XML element corresponds to an actual tag in the source:
        <xref id='...'>, <p chance='...'>, <choice>, etc.
        Each element type is handled in its own method.  Like we did in
        parse(), we construct a method name based on the name of the
        element ("do_xref" for an <xref> tag, etc.) and
        call the method.
        """
        handlerMethod = getattr(self, "do_%s" % node.tagName)
        handlerMethod(node)
        
    def parse_Comment(self, node):
        """parse a comment
        
        The grammar can contain XML comments, but we ignore them
        """
        pass
    
    def do_latex_xml(self, doc_node):
        
        preamble = []
        macros = []
        
        for node in doc_node.childNodes:
            name = node.nodeName
            
            if name == "macros":
                print "macros tag detected."
                for child in node.childNodes:
                    if child.nodeName == "file":
                        print "\tfile tag detected."
                        source = child.firstChild.data.strip()
                        try:
                            macros_file = toolbox.openAnything(source)
                            macros.append(macros_file.read())
                            macros_file.close()
                            print "\t\tSuccesfully read macros file."
                        except:
                            print "\t\terror in opening macro file."
                    else:
                        if child.nodeName ==  "#text":
                            stripped = child.data.strip()
                            if len(stripped) > 0:
                                macros.append(stripped)
            
            
            if name == "preamble":
                print "preamble tag detected."
                for child in node.childNodes:
                    if child.nodeName == "file":
                        print "\tfile tag detected."
                        source = child.firstChild.data.strip()
                        try:
                            preamble_file = toolbox.openAnything(source)
                            preamble.append(preamble_file.read())
                            preamble_file.close()
                            print "\t\tSuccesfully read preamble file."
                        except:
                            print "\t\terror in opening preamble file."
                    else:
                        if child.nodeName ==  "#text":
                            stripped = child.data.strip()
                            if len(stripped) > 0:
                                preamble.append(stripped)


        
        if len(macros) == 0:
            macros_file = toolbox.openAnything(default_macros)
            macros.append(macros_file.read())
            macros_file.close()

        if len(preamble) == 0:
            preamble_file = toolbox.openAnything(default_preamble)
            preamble.append(preamble_file.read())
            preamble_file.close()
        
        self.tex_lines.extend(preamble)
        self.tex_lines.extend(macros)
        
        for node in doc_node.childNodes:
            name = node.nodeName
            if name == "document":
                self.parse(node)


    
    def do_document(self, node):
        
        self.tex_lines.append("\\begin{document}\n")
        
        for k,child_node in enumerate(node.childNodes):
            if child_node is not None:
                if child_node.nodeName == "title":
                    self.parse(child_node)
                    node.childNodes[k] = None
        
        for k,child_node in enumerate(node.childNodes):
            if child_node is not None:
                if child_node.nodeName == "author":
                    self.parse(child_node)
                    node.childNodes[k] = None
                
        for child_node in node.childNodes:
            if child_node is not None:
                self.parse(child_node)
        
        self.tex_lines.append("\\end{document}\n")
    
    def do_title(self, node):
        
        text = []
        for child_node in node.childNodes:
            text.append(child_node.data.strip())
        
        self.tex_lines.append("\\begin{center} \n { \\bf ")
        self.tex_lines.extend(text)
        self.tex_lines.append("} \\end{center}")
    
    def do_author(self, node):
        text = []
        for child_node in node.childNodes:
            text.append(child_node.data.strip())
        
        self.tex_lines.append("\\begin{center} \n ")
        self.tex_lines.extend(text)
        self.tex_lines.append("\\end{center}")

    def do_discussion(self, node):
        text = []
        for child_node in node.childNodes:
            text.append(child_node.data.strip())
        
        self.tex_lines.append("\\begin{flushleft} \n ")
        self.tex_lines.extend(text)
        self.tex_lines.append("\\end{flushleft}")
    
    def do_definition(self, node):
        
        self.tex_lines.append("\\begin{flushleft} \n ")
        for child in node.childNodes:
            self.parse(child)
        self.tex_lines.append("\\end{flushleft}")

    def do_equation(self, node):
        text = []
        for child_node in node.childNodes:
            text.append(child_node.data.strip())
        
        self.tex_lines.append("\\begin{equation} \n ")
        self.tex_lines.extend(text)
        self.tex_lines.append("\\end{equation}")
        
    def do_section(self, node):
        
        self.tex_lines.append("\\begin{flushleft}\n")
        
        for k,child_node in enumerate(node.childNodes):
            if child_node is not None:
                if child_node.nodeName == "number":
                    self.tex_lines.append("{\\bf ")
                    for gchild_node in child_node.childNodes:
                        self.parse(gchild_node)
                    self.tex_lines.append(" }")
                    node.childNodes[k] = None
        
        for k,child_node in enumerate(node.childNodes):
            if child_node is not None:
                if child_node.nodeName == "name":
                    self.tex_lines.append("{\\bf ")
                    for gchild_node in child_node.childNodes:
                        self.parse(gchild_node)
                    self.tex_lines.append(" }")
                    node.childNodes[k] = None
        
        self.tex_lines.append("\\end{flushleft}\n")

    def do_itemize(self, node):
        self.tex_lines.append("\\begin{itemize} \n ")
        for child_node in node.childNodes:
            if child_node.nodeName == "#text":                
                text = child_node.data
                print len((text.split('\n')))
                print text.__class__
                if len(text)>0:
                    self.tex_lines.append("\\item")
                    self.tex_lines.append(text)
        quit()
        self.tex_lines.append("\n\\end{itemize} \n ")
    
    def do_theorem(self, node):
        
        fields = {}
        for child_node in node.childNodes:
            name = child_node.nodeName
            if name != "#text":
                fields[name] = child_node
        
        if "name" in fields:
            thm_name = fields["name"].firstChild.data.strip()
            self.tex_lines.append("{\\bf Theorem: (" + thm_name  + ")}")

        else:
            self.tex_lines.append("{\\bf Theorem: }")  
        
        
    def do_corollary(self, node):
        
        fields = {}
        for child_node in node.childNodes:
            name = child_node.nodeName
            if name != "#text":
                fields[name] = child_node
        
        if "name" in fields:
            thm_name = fields["name"].firstChild.data.strip()
            self.tex_lines.append("{\\bf Corollary: (" + thm_name  + ")}")

        else:
            self.tex_lines.append("{\\bf Corollary: }")  





class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_all(self):
        pass






if __name__ == "__main__":
    
    args = sys.argv[1:]
    
    if len(args) == 0:
        print "Running unittests."
        unittest.main()
    
    
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
            (name, in_ext) = os.path.splitext(ifname)
            output_args[k] = name + '.out' + '.tex'
    
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
        
        texer = to_tex(input)
        tex_lines = texer.process()
        
        for line in tex_lines:
            #print line
            output.write(line + "\n" )
        
        output.close()
        input.close()
        





