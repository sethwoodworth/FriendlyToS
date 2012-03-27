# HTML -> Markdown translation functions
# All of these functions assume that the provided element does not have child 
# elements.

from lxml.html import HtmlElement
import lxml.html
import re

class MarkdownTranslator(object):
    translator = dict()             # Element translator functions

    # Define which elements are block level, cause they're special
    block_level = {'div','h1','h2','h3','h4','h5','h6','li','ol','p','pre','ul'}

    # Build the dictionary of element translators

    # Lists
    # In the normal case, these are dumb translators. In the case of nested
    # lists, we need to prevent the inclusion of additional new lines. Thus,
    # the last li of a nested list does not add a newline, and nested uls and 
    # ols add fewer newlines.
    # Additional work takes place in translate()
    def translate_li(el):
        if el.getparent().getparent() is not None \
                and el.getparent().getparent().tag == 'li' \
                and el.getparent().iterchildren(tag='li', reversed=True).next() is el:
            return el.text_content()
        else:
            return "" + el.text_content() + "\n"

    translator['li'] = translate_li
    def translate_ul(el):
        if el.getparent().tag == 'li':
            return "\n" + el.text_content()
        else:
            return "\n\n" + el.text_content() + "\n\n"

    translator['ul'] = translate_ul
    translator['ol'] = translator['ul']

    # Links
    # Markdown links don't work with newlines.
    def translate_a(el):
        if 'href' in el.keys():
            if re.match(r"^javascript\:.*$", el.attrib['href']):
                # Links that call javascript break markdown. Also, they just
                # won't work on ftos. Just print the text.
                return el.text_content()
            # A good old link. Need to remove any newlines that might be in it.
            return "[" + el.text_content().replace('\n','') \
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
    
    # Line Breaks
    translator['br'] = lambda(el) : "\n\n"

    # A p or div tag, that is the first non-whitespace content of an li, needs
    # to appear on the same line as the * indicating a list item. So we need
    # to remove the whitespace before a p or div in this case.
    def translate_p(el):
        if el.getparent().tag == 'li' and el.getprevious() is None \
                and (el.getparent().text is None or \
                el.getparent().text.strip() == ''):
            el.getparent().text = ''
        return el.text_content() + "\n\n"
            
    # <p> and <div> are the samething for this translation
    translator['p'] = translate_p 
    translator['div'] = translator['p']

    # Span elements
    translator['span'] = lambda(el) : el.text_content()

    # <b> and <strong> are the same
    # MD breaks when there is spacing between the markup and the content
    translator['b'] = lambda(el) : "**" + el.text_content().strip() + "**"
    translator['strong'] = translator['b']

    # <i> and <em> are the same
    # MD breaks when there is spacing between the markup and the content
    translator['i'] = lambda(el) : "*" + el.text_content().strip() + "*"
    translator['em'] = translator['i']

    # <u>
    # MD doesn't do underlines, so just return the text
    translator['u'] = lambda(el) : el.text_content()

    # Images
    translator['img'] = lambda(el) : "![" + el.attrib['alt'] + "](" + el.attrib['src'] + ")"

    # Headings
    translator['h1'] = lambda(el) : "#" + el.text_content() + "\n\n"
    translator['h2'] = lambda(el) : "##" + el.text_content() + "\n\n"
    translator['h3'] = lambda(el) : "###" + el.text_content() + "\n\n"
    translator['h4'] = lambda(el) : "####" + el.text_content() + "\n\n"
    translator['h5'] = lambda(el) : "#####" + el.text_content() + "\n\n"
    translator['h6'] = lambda(el) : "######" + el.text_content() + "\n\n"

    # Probably need to add more to the <pre> function
    translator['pre'] = lambda(el) : el.text_content().replace("\n", " ") + "\n\n"

    # Unknown tag. OMG, what is it?!?!
    translator['fud'] = lambda(el) : el.text_content()

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

    def translate(self, el):
        """
            Function called by others to translate an lxml.html.HtmlElement 
            into a string of Markdown
            CAUTION: This will modify, mangle, and pretty much destroy el. 
            TODO: Make this not modify, mangle, and pretty much destroy el.
        """

        if not isinstance(el, HtmlElement):
            raise ValueError("Expecting lxml.HtmlElement, received " \
                            + `type(el)`)

        if self.verbose == True:
            self.v_prepend += "  "
            print self.v_prepend + "Tag: " + el.tag
            print self.v_prepend + "Number of Children: " + `len(el)`
            print self.v_prepend + "List level " + `self.list_level`

        # Translate depth first
        i = 1   # Used to numerate ols
        for child in el.iterchildren():
            # Skip comments
            if isinstance(child, lxml.html.HtmlComment): continue


            # Whitespace before block level elements mess up indentation.
            # If the element has a left sibling, the whitespace will be in tail
            # Otherwise, the whitespace will be in the parent's text
            left_sib = child.getprevious()
            if (child.tag in MarkdownTranslator.block_level):
                if left_sib is not None:
                    left_sib.tail = left_sib.tail.rstrip(' \t')
                elif el.text is not None:
                    el.text = el.text.rstrip(' \t')

            # Whitespace between lis mess up indentation.
            if child.tag == 'li' and child.tail is not None:
                child.tail = child.tail.strip()

            if el.tag == 'ul' and child.tag == 'li' and self.tl:
                #self.prepend += "  "
                #self.list_level += 1
                translated = self.translate(child)
                #self.prepend = self.prepend[:-2]
                #child.text = self.prepend + " * " + translated
                child.text = self.indent_list(True) + "* " + translated
                #self.list_level -= 1
            elif el.tag == 'ol' and child.tag == 'li' and self.tl:
                #self.prepend += "  "
                #self.list_level += 1
                translated = self.translate(child)
                #self.prepend = self.prepend[:-2]
                #child.text = self.prepend + " " + `i` + ". " + translated
                child.text = self.indent_list(True) + `i` + ". " + translated
                #self.list_level -= 1
                i += 1
            else:
                #child.text = self.translate(child)
            #child.text = self.prepend + self.translate(child)
                if child.tag in {'ol','ul'}:
                    self.list_level += 1
                    child.text = self.translate(child)
                    self.list_level -= 1
                elif child.tag in (MarkdownTranslator.block_level - {'ol','ul'}):
                    child.text = self.indent_list(False) + self.translate(child)
                else:
                    child.text = self.translate(child)
                    # Don't let brs brake list indentation
                    if child.tag == 'br':
                        if self.verbose == True:
                            print self.v_prepend + "Adding list indentation after br"
                        if child.tail:
                            child.tail = self.indent_list(False) + child.tail.strip()

            child.drop_tag()    # Causes text to be absorbed into the parent

        if self.verbose: 
            print self.v_prepend + "Calling '" + el.tag + "' translator"
            self.v_prepend = self.v_prepend[:-2]
        
        # By now the text of all children have been absorbed into the text of
        # this element. Now all that is left is to translate the element
        # itself. If we are not translating lists, then we need to add list
        # markup to the translation.
        #
        # It seems that nested lists require some cleanup. There needs to b
        # 3 \n between the end of a nested list's content and the beginning of
        # and element of the outer list. Thus, some regexing may be needed.
        #
        # 
        if el.tag not in MarkdownTranslator.translator:
            translated = MarkdownTranslator.translator['fud'](el)
        else:
            translated = MarkdownTranslator.translator[el.tag](el)

        if el.tag == 'li' and self.tl == False:
            el.text = '<li>' + translated + '</li>'
        elif el.tag == 'ol' and self.tl == False:
            el.text = '<ol>' + translated + '</ol>'
        elif el.tag == 'ul' and self.tl == False:
            el.text = '<ul>' + translated + '</ul>'
        else:
            el.text = translated

        # Lets play with encoding!
        # TODO: Consider if there is a better place/way to handle this
        el.text = el.text.replace(u'\xc2\xa0', '&nbsp;')

        return el.text

