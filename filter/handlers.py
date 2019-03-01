class Handler:
    """
    An object that handles method calls from the Parser.

    The Parser will call the start() and end() methods at the
    beginning of each block, with the proper block name as a
    parameter. The sub() method will be used in regular expression
    substitution. When called with a name such as 'emphasis', it will
    return a proper substitution function.
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method): return method(*args)
    def start(self, name):
        self.callback('start_', name)
    def end(self, name):
        self.callback('end_', name)
    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: match.group(0)
            return result
        return substitution

class HTMLRenderer(Handler):
    """
    A specific handler used for rendering HTML.

    The methods in HTMLRenderer are accessed from the superclass
    Handler's start(), end(), and sub() methods. They implement basic
    markup as used in HTML documents.
    """
    def start_document(self):
        print('<html><head><meta charset="utf-8"/><title>...</title></head><body>')
    def end_document(self):
        print('</body></html>')
    def start_paragraph(self):
        print('\n')
    def end_paragraph(self):
        print('\n')
    def start_heading(self):
        print('##')                                                                              
    def end_heading(self):
        print('\n\n')
    def start_list(self):
        print('\n')
    def end_list(self):
        print('\n')
    def start_listitem(self):
        print('<li>')
    def end_listitem(self):
        print('</li>')
    def start_title(self):
        print('<h1>')
    def end_title(self):
        print('</h1>')
    def sub_emphasis(self, match):
        return '<em>{}</em>'.format(match.group(1))
    def sub_url(self, match):
        return '<a href="{}">{}</a>'.format(match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:{}">{}</a>'.format(match.group(1), match.group(1))
    
    def sub_redundant_space(self, match):
        return ' '
    
    def sub_begin_space(self, match):
        return 'ZXCV'

    def sub_redundant_newlines(self, match):
        return 'HEJ'
    
    def sub_hyphen_blank(self, match):
        return 'QWERTY'

    def sub_less_than(self, match):
        # Substitute '<' (less than) characters
        return ' _LESSTHAN_ '
    
    def sub_greater_than(self, match):
        # Substitute '>' (greater than) characters
        return ' _GREATERTHAN_ '

    def sub_linefeed(self, match):
        return '\n<pb/>\n'
    
    def sub_ampersand(self, match):
        # Substitute ampersand characters with entity
        return ' &amp; '

    def sub_non_breaking_hyphen(self, match):
        # Substitute non-breaking hyphens with regular hyphens
        return '‐'

    def sub_indent_for_paragraph(self, match):
        return format(match.group(1)) + '\n\n' + format(match.group(2))
    
    def sub_number_pagebreak(self, match):
        # Substitute a pagebreak in print edition with xml pagebreak element
        return ' <pb n="{}{}"/> '.format(match.group(1), match.group(2))

    def sub_left_lc(self, match):
        # Substitute line counter in left margin 
        return '\n' + format(match.group(1))
    
    def sub_right_lc(self, match):
        # Substitute line counter in right margin
        return '\n'
    
    #def sub_norm_left_ms_pb(self, match):
        # Normalize manuscript page in left margin
        #return ' _MSPB_{}{}{}_'+ format(match.group(1))

    def sub_ms_pb(self, match):
        # Substitute manuscript pagebreaks '||' with xml pagebreak element
        return ' <pb ed="nil"/> '

    def sub_left_ms_pb(self, match):
        # Insert manuscript page break numbers found in left margin in n attribute 
        return '\n' + format(match.group(2)) + ' <pb ed="nil" n="{}"/> '.format(match.group(1)) + format(match.group(3))
    
    def sub_right_ms_pb(self, match):
        # Insert manuscript page break numbers found in right margin in n attribute 
        return '\n' + format(match.group(1)) + ' <pb ed="nil" n="{}"/> '.format(match.group(3)) + format(match.group(2))

    def feed(self, data):
        print(data)
