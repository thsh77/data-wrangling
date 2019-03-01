import sys, re, ipdb
from handlers import *
from util import *
from rules import *

class Parser:
    """
    A Parser reads a text file, applying rules and controlling a handler.
    """
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []
    def addRule(self, rule):
        self.rules.append(rule)
    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, 
                    self.handler)
                    if last: break
        self.handler.end('document')

class BasicTextParser(Parser):
    """
    A specific Parser that adds rules and filters in its constructor.
    """
    def __init__(self, handler):
        Parser.__init__(self, handler)
        #self.addFilter(r'(\x0C)', 'linefeed')
        #self.addRule(ListRule())
        #self.addRule(ListItemRule())
        #self.addRule(TitleRule())
        #self.addRule(HeadingRule())        
        self.addRule(ParagraphRule())
        
        #self.addFilter(r'\*(.+?)\*', 'emphasis')
        #self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        #self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


        #self.addFilter(r'\*(.+?)\*', 'emphasis')
        #self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        #self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')
        

        """Filters for text clean-up"""
        # Reduce whitespace and tabs; in each of the two ranges below there is a blank and a tab
        self.addFilter(r'[     ][  ]+', 'redundant_space')

        #Reduce whitespace in beginning of lines
        self.addFilter(r'^', 'begin_space')

        # Reduce sequential empty lines to one
        #self.addFilter(r'\n', 'redundant_newlines')

        # Filter non-breaking hyphens
        self.addFilter(r'\u00AD', 'non_breaking_hyphen')
        
        # Remove blank lines after hyphen
        #self.addFilter(r'‐\n\s*[a-z]', 'hyphen_blank')

        # Filter < characters
        self.addFilter(r'<', 'less_than')

        # Filter > characters
        self.addFilter(r'>','greater_than')

        # Filter linecount in left margin
        self.addFilter(r'\s{0,3}[1-5]?[05]\s{1,3}([A-ZÆØÅa-zæøå0-9])', 'left_lc')
        
        # Filter linecount in right margin
        self.addFilter(r'\s[1-5][05]?$', 'right_lc')

        # Normalize manuscript pagebreaks in left margin
        #self.addFilter(r'\s*(A-L)+\s*(\d{0,2})\s*([rvRV])', 'norm_left_ms_pb')

        """Filters for formatting"""

        # Filter linefeed characters
        self.addFilter(r'(\x0C)', 'linefeed')   
        
        # Filter & characters
        self.addFilter(r'\&', 'ampersand')
        
        
        
        # Filter indented lines
        self.addFilter(r'([.!«])\n\s*?([A-ZÆØÅ0-9])', 'indent_for_paragraph')
        
        # Filter pagebreaks
        self.addFilter(r'.*\n.*\n<pb/>\n(\d{0,4})?\s*[A-ZÆØÅ][A-ZÆØÅ\s]+(\d{0,4})?', 'number_pagebreak')      

        # Substitute manuscript pagebreaks
        self.addFilter(r'[\|I]\s*[\|I]', 'ms_pb')
        
        # Filter manuscript pagebreaks in left margin
        self.addFilter(r'\s*([A-L]+\s*\d{0,2}\s*[rvRV])(.*)<pb ed="nil"/>(.*)', 'left_ms_pb')
        
        # Filter manuscript pagebreaks in right margin
        self.addFilter(r'(.*)<pb ed="nil"/>(.*)([A-L]+\s*\d{0,2}\s*[rvRV])', 'right_ms_pb')

handler = HTMLRenderer()
parser = BasicTextParser(handler)

parser.parse(sys.stdin)