# HTML -> Markdown translation functions
# All of these functions, except for the ul and ol functions, assume that 
# the provided element does not have child elements.

from lxml.html import HtmlElement

class MarkdownTranslator(object):
    translator = dict()             # Element translator functions


    # Build the dictionary of element translators

    # Lists
    translator['li'] = lambda(el) : "" + el.text_content() + "\n"
    # ul and ol are dumb translators, since all the real work happens in 
    # translate()
    translator['ul'] = lambda(el) : el.text_content() + "\n"
    translator['ol'] = translator['ul']

    # Links
    # Markdown links don't work with newlines.
    translator['a'] = lambda(el) : "[" + el.text_content().replace('\n','') \
                        +  "](" + el.attrib['href'] + ")"

    # Line Breaks
    translator['br'] = lambda(el) : "\n\n"

    # <p> and <div> are the samething for this translation
    translator['p'] = lambda(el) : el.text_content() + "\n\n"
    translator['div'] = translator['p']

    # Span elements
    translator['span'] = lambda(el) : el.text_content()

    # <b> and <strong> are the same
    translator['b'] = lambda(el) : "**" + el.text_content() + "**"
    translator['strong'] = translator['b']

    # <i> and <em> are the same
    translator['i'] = lambda(el) : "*" + el.text_content() + "*"
    translator['em'] = translator['i']

    # Images
    translator['img'] = lambda(el) : "![" + el.attrib['alt'] + "](" + el.attrib['src'] + ")"

    # Headings
    translator['h1'] = lambda(el) : "#" + el.text_content() + "#"
    translator['h2'] = lambda(el) : "##" + el.text_content() + "##"
    translator['h3'] = lambda(el) : "###" + el.text_content() + "###"
    translator['h4'] = lambda(el) : "####" + el.text_content() + "####"
    translator['h5'] = lambda(el) : "#####" + el.text_content() + "#####"
    translator['h6'] = lambda(el) : "######" + el.text_content() + "######"

    # Probably need to add more to the <pre> function
    translator['pre'] = lambda(el) : el.text_content().replace("\n", " ") + "\n\n"

    # End element translator functions

    def __init__(self, verbose=False):
        """
            If verbose == True, debugging messages will be printed out during a 
            translation
        """
        self.prepend = ""       # Used in ul and ol
        self.v_prepend = ""     # Used during verbose printing
        self.verbose = verbose

    def translate(self, el):
        """
            Function called by others to translate an lxml.html.HTMLElement 
            into a string of Markdown
            CAUTION: This will modify, mangle, and pretty much destroy el. 
            TODO: Make this not modify, mangle, and pretty much destroy el.
        """
        if self.verbose == True:
            self.v_prepend += "  "
            print self.v_prepend + "Tag: " + el.tag
            print self.v_prepend + "Number of Children: " + `len(el)`

        # Translate depth first
        i = 1
        for child in el.iterchildren():

            if el.tag == 'ul' and child.tag == 'li':
                self.prepend += "  "
                translated = self.translate(child)
                self.prepend = self.prepend[:-2]
                child.text = self.prepend + " * " + translated
            elif el.tag == 'ol' and child.tag == 'li':
                self.prepend += "  "
                translated = self.translate(child)
                self.prepend = self.prepend[:-2]
                child.text = self.prepend + " " + `i` + ". " + translated
                i += 1
            else:
                child.text = self.translate(child)
            child.drop_tag()    # Causes text to be absorbed into the parent

        if self.verbose: 
            print self.v_prepend + "Calling '" + el.tag + "' translator"
            self.v_prepend = self.v_prepend[:-2]
        
        # By now the text of all children have been absorbed into the text of
        # this element. Now all that is left is to translate the element
        # itself. 
        el.text = MarkdownTranslator.translator[el.tag](el)
        return el.text

