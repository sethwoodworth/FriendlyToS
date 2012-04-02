# HTML -> Markdown translation functions
# All of these functions assume that the provided element does not have child 
# elements.

from lxml.html import HtmlElement
from lxml.html.clean import Cleaner
import lxml.html
import re
import codecs

class MarkdownTranslator(object):
    translator = dict()             # Element translator functions

    # Define which elements are block level, cause they're special
    # Maybe poor name - this set refers to HTML elements that will cause newlines in MD.
    block_level = {'blockquote','br','dd','div','dl','h1','h2','h3','h4','h5','h6','li','ol','p','pre','td','ul'}

    # Build the dictionary of element translators

    # ------Lists------
    # In the normal case, these are dumb translators. In the case of nested
    # lists, we need to prevent the inclusion of additional new lines. Thus,
    # the last li of a nested list does not add a newline, and nested uls and 
    # ols add fewer newlines.
    # Additional work takes place in recursiveTranslate()
    def translate_li(self, el):
        if el.getparent().getparent() is not None \
                and el.getparent().getparent().tag == 'li' \
                and el.getparent().iterchildren(tag='li', reversed=True).next() is el:
            return el.text_content().strip()
        else:
            return el.text_content().strip() + "\n"

    translator['li'] = translate_li
    translator['dd'] = translator['li']

    def translate_ul(self, el):
        if el.getparent() is not None and el.getparent().tag == 'li':
            return "\n" + el.text_content()
        else:
            return "\n\n" + el.text_content() + "\n\n"

    translator['ul'] = translate_ul
    translator['ol'] = translator['ul']
    translator['dl'] = translator['ul']

    # ------Links------
    # Markdown links don't work with newlines.
    def translate_a(self, el):
        if 'href' in el.keys():
            if re.match(r"^javascript\:.*$", el.attrib['href']):
                # Links that call javascript break markdown. Also, they just
                # won't work on ftos. Just print the text.
                return el.text_content()
            # A good old link. Need to remove any newlines that might be in it.
            return "[" + el.text_content().replace('\n',' ') \
                +  "](" + el.attrib['href'] + ")"
        elif 'name' in el.keys():
            # Must be an anchor. Leave it as is.
            #TODO Pass a constant for encoding
            #TODO Define an encoding constant someplace accessible to all
            return lxml.html.tostring(el, encoding='utf-8', method='html')
        else:
            # What the hell is this? Just print out the text
            return el.text_content()

    translator['a'] = translate_a
    
    # ------Line Breaks------
    translator['br'] = lambda self,el : "\n\n" 

    # ------Paragraphs and Divs------
    # A p or div tag, that is the first non-whitespace content of an li, needs
    # to appear on the same line as the * indicating a list item. So we need
    # to remove the whitespace before a p or div in this case.
    def translate_p(self,el):
        if el.getparent().tag == 'li' and el.getprevious() is None \
                and (el.getparent().text is None or \
                el.getparent().text.strip() == ''):
            #el.getparent().text = ''
            rtn_str = el.text_content().strip()
        else:
            rtn_str = "\n\n" + self.indent_list(False) + el.text_content().strip()
        return rtn_str + "\n\n"
            
    # <p> and <div> are the samething for this translation
    translator['p'] = translate_p 
    translator['div'] = translator['p']

    # ------Span------
    translator['span'] = lambda self,el : el.text_content()

    # ------Bold and Strong------
    # MD breaks when there is spacing between the markup and the content
    # MD Bold doesn't work across line breaks, so wrap seperate paragraphs in their own bolds
    translator['b'] = lambda self,el : "**" + re.sub(r'\n{2,}', '**\n\n' + self.indent_list(False) + '**', el.text_content().strip()) + "**"
    translator['strong'] = translator['b']

    # ------Italics and Emphasis------
    # MD breaks when there is spacing between the markup and the content
    translator['i'] = lambda self,el : "*" + re.sub(r'\n{2,}', '*\n\n' + self.indent_list(False) + '*', el.text_content().strip()) + "*"
    translator['em'] = translator['i']

    # ------<u>------
    # MD doesn't do underlines, so just return the text
    #translator['u'] = lambda self,el : el.text_content()

    # ------Images------
    translator['img'] = lambda self,el : "![" + el.attrib['alt'] + "](" + el.attrib['src'] + ")"

    # ------Headings------
    def pre_heading(self,el):
        # Headers should not have newlines in them
        # el.text = el.text.replace('\n', ' ')

        # Special case of a heading being the first content of an li.
        parent = el.getparent()
        left_sib = el.getprevious()
        if parent and parent.tag == 'li' and left_sib is None \
                and (parent.text is None or parent.text.strip() == ''):
            return ''
        return "\n" + self.indent_list(False)

    translator['h1'] = lambda self,el : self.pre_heading(el) + "#" + el.text_content() + "\n\n"
    translator['h2'] = lambda self,el : self.pre_heading(el) + "##" + el.text_content() + "\n\n"
    translator['h3'] = lambda self,el : self.pre_heading(el) + "###" + el.text_content() + "\n\n"
    translator['h4'] = lambda self,el : self.pre_heading(el) + "####" + el.text_content() + "\n\n"
    translator['h5'] = lambda self,el : self.pre_heading(el) + "#####" + el.text_content() + "\n\n"
    translator['h6'] = lambda self,el : self.pre_heading(el) + "######" + el.text_content() + "\n\n"

    # ------Preformated------
    # Probably need to add more to the <pre> function
    translator['pre'] = lambda self,el : "\n" + self.indent_list(False) + el.text_content().replace("\n", " ") + "\n\n"

    # ------Blockquotes------
    def translate_blockquote(self,el):
        parent = el.getparent()
        rtn_str = ""
        for line in el.text_content().strip().split("\n"):
            rtn_str += self.indent_list(False) + "> " + line.strip() + "\n"
        return rtn_str + "\n\n"
    translator['blockquote'] = translate_blockquote

    # ------Tables------
    # MD doesn't have tables, so default behavior should be to just pass a
    # table through. But, some sites use table tags inappropriately as elements.
    # recursive_translate() takes care of proper tables. These translators will
    # only be called when they are used outside of a table.

    translator['td'] = translator['p']      
    translator['th'] = translator['td']
    translator['tr'] = lambda self,el : el.text_content()
    translator['thead'] = translator['tr']
    translator['tbody'] = translator['tr']
    translator['tfoot'] = translator['tr']
    translator['colgroup'] = lambda self,el : el.text_content()
    translator['col'] = translator['colgroup']

    # Unknown tag. OMG, what is it?!?!
    translator['fud'] = lambda self,el : el.text_content()

    # End element translator functions

    # Creates the appropriate indentation level.
    # No indentation is added if not in a list.
    # A level 1 li is indented by 2 spaces
    # All other level lis are indented by 4 + the previous level's indent
    # Note the difference indentation between an li and the content of that li
    def indent_list(self, li):
        if self.list_level == 0: return ''
        list_level = self.list_level
        if li == True: list_level -= 1
        return ' ' * (2 + (4 * list_level))

    # For a block level element, the text of its parent that follows must be
    # indented to maintain lists.
    def post_block(self, el):
        if el.tail:
            if self.verbose:
                print self.v_prepend + "Indenting tailing parent text"
            el.tail = self.indent_list(False) + el.tail

    # Function which does the real work of translating.
    # Depth-first traversal of a tree, in the form of lxml.html.HtmlElement
    def recursiveTranslate(self, el):
        if not isinstance(el, HtmlElement):
            raise ValueError("Expecting lxml.HtmlElement, received " \
                            + `type(el)`)

        if self.verbose == True:
            self.v_prepend += "  "
            print self.v_prepend + "Tag: " + el.tag
            print self.v_prepend + "Number of Children: " + `len(el)`
            print self.v_prepend + "List level " + `self.list_level`

        # For certain tags, skip translation entirely
        if el.tag in {'table'}:
            return lxml.etree.tostring(el, encoding=unicode, method='html')

        # Translate depth first
        i = 1   # Used to numerate ols
        for child in el.iterchildren():

            # Lists require a bit of extra handling
            if el.tag == 'ul' and child.tag == 'li' and self.tl:
                translated = self.recursiveTranslate(child)
                child.text = self.indent_list(True) + "* " + translated
            elif el.tag == 'ol' and child.tag == 'li' and self.tl:
                translated = self.recursiveTranslate(child)
                child.text = self.indent_list(True) + `i` + ". " + translated
                i += 1
            else:
                if child.tag in {'ol','ul'}:
                    self.list_level += 1
                    child.text = self.recursiveTranslate(child)
                    self.list_level -= 1
                else:
                    child.text = self.recursiveTranslate(child)

            child.drop_tag()    # Causes text to be absorbed into the parent

        if self.verbose: 
            print self.v_prepend + "Calling '" + el.tag + "' translator"
            self.v_prepend = self.v_prepend[:-2]
        
        # By now the text of all children have been absorbed into the text of
        # this element. Now all that is left is to translate the element
        # itself. If we are not translating lists, then we need to add list
        # markup to the translation.
        if el.tag not in MarkdownTranslator.translator:
            translated = MarkdownTranslator.translator['fud'](self,el)
        else:
            translated = MarkdownTranslator.translator[el.tag](self,el)

        # Add indentation to parent text that follows a block level element
        if el.tag in MarkdownTranslator.block_level:
            self.post_block(el)

        if el.tag == 'li' and self.tl == False:
            el.text = '<li>' + translated + '</li>'
        elif el.tag == 'ol' and self.tl == False:
            el.text = '<ol>' + translated + '</ol>'
        elif el.tag == 'ul' and self.tl == False:
            el.text = '<ul>' + translated + '</ul>'
        else:
            el.text = translated

        return el.text

    def __init__(self, tl=True, verbose=False):
        """
            If tl == True, the translate funciton will translate list markup 
            into Markdown.
            If verbose == True, debugging messages will be printed out during a 
            translation
        """
        if not isinstance(tl, bool):
            raise ValueError("Expecting bool")
        if not isinstance(verbose, bool):
            raise ValueError("Expecting bool")

        self.prepend = ""       # Used in ul and ol
        self.list_level = 0
        self.v_prepend = ""     # Used during verbose printing
        self.verbose = verbose
        self.tl = tl

    def setTranslateLists(self, tl):
        """
           Use to set an instance of MarkdownTranslator to translate uls and
           ols. If given False, the translate function will not translate lists
           and will retain the HTML of ul, ol, and li, but will continue to 
           translate child elements.

           INPUT: True or False
           DEFAULT: True
        """
        if not isinstance(tl, bool):
            raise ValueError("Expecting bool, received " + `type(tl)`)

        self.tl = tl
        return

    def translate(self, html):
        """
            Function called by others to translate HTML into Markdown
            Input can be either a string or an lxml.html.HtmlElement
            CAUTION: This will modify, mangle, and pretty much destroy el. 
            TODO: Make this not modify, mangle, and pretty much destroy el.
        """
        # If lxml.html.HtmlElement, turn it into text
        if isinstance(html, HtmlElement):
            html_str = lxml.etree.tostring(html, encoding=unicode, method='html')
        elif isinstance(html, str):
            html_str = html
        else:
            raise ValueError("Expecting str or lxml.HtmlElement, received " \
                            + `type(html)`)

        # Escape Markdown characters and remove some tags
        html_str = html_str.replace('[','\[').replace(']','\]')
        c = Cleaner(forms=False, annoying_tags=False, remove_tags=['u'])
        html_str = c.clean_html(html_str)

        # Turn into a tree using a parser that removes whitespace, which doesn't
        # seem to actually do anything.
        psr = lxml.html.HTMLParser(remove_blank_text=True)
        el = lxml.html.fromstring(html_str, parser=psr)

        for node in el.iter():
            # Remove whitespace surrounding any block level elements
            if node.tag in MarkdownTranslator.block_level:
                left_sib = node.getprevious()
                parent = node.getparent()
                # Remove whitespace to the left
                if left_sib:
                    # left_sib.tail == None indicates there is no whitespace,
                    # our goal condition. So don't do anything.
                    if left_sib.tail:
                        left_sib.tail = left_sib.tail.rstrip()
                elif parent and parent.text:
                        parent.text = parent.text.rstrip()
                # Remove whitespace to the right
                if node.tail:
                    node.tail = node.tail.lstrip()

            # Remove newlines inside of blocklevels, except for pre and blockquote
            if node.tag in MarkdownTranslator.block_level - {'blockquote','pre'} and node.text:
                node.text = ' '.join(node.text.split('\n'))
            if parent and parent.tag in MarkdownTranslator.block_level - {'blockquote','pre'} and node.tail:
                node.tail = ' '.join(node.tail.split('\n'))
                

        # For debugging, its helpful to save the string we are about to translate
        if self.verbose:
            f = codecs.open('clean_html.html','w','utf-8')
            f.write(lxml.etree.tostring(el, encoding=unicode, method='html'))
            f.close()
        
        # Commence Recursing!
        md_str = self.recursiveTranslate(el)

        # Replace some unicode
        # Not sure why --- I hate text encoding
        md_str = md_str.replace(u'\xc2\xa0', '&nbsp;')

        return md_str
        

