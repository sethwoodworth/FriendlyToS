# Process for adding cases to the test_files test:
#   1.) Be in a python shell
#   2.) from scrape import *
#   3.) from lxml import etree
#   4.) tosDoc = fetch('<document name>')
#   5.) results = html.fromstring(tosDoc).xpath(xpaths['<document name>'])
#   6.) elHtml = etree.tostring(results[0])
#   7.) md = t.translate(results[0])
#   8.) saveTestCase(elHtml, md, '<document name>')

from MarkdownTranslator import *
from lxml.html import fromstring
import unittest

# Tests
class TestMarkdownTranslator(unittest.TestCase):
    def setUp(self):
        self.t = MarkdownTranslator(True,False)
        self.samples_dir = './samples/'
    def tearDown(self):
        pass
    def test_a_translator(self):
        print "Testing 'a' translator...",
        el = fromstring('<a href="http://www.friendlytos.org">Friendly ToS</a>')
        correct_response = '[Friendly ToS](http://www.friendlytos.org)'
        response = self.t.translate(el)
        err_msg = 'Links are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_b_translator(self):
        print "Testing 'b' translator...",
        el = fromstring('<b>Text</b>')
        correct_response = '**Text**'
        response = self.t.translate(el)
        err_msg = 'Bolds are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_br_translator(self):
        print "Testing 'br' translator...",
        el = fromstring('<br><br />')
        correct_response = '\n\n\n\n'
        response = self.t.translate(el)
        err_msg = 'Line breaks are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_div_translator(self):
        print "Testing 'div' translator...",
        el = fromstring('<div>Text!</div>')
        correct_response = 'Text!\n\n'
        response = self.t.translate(el)
        err_msg = 'Divs are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_em_translator(self):
        print "Testing 'em' translator...",
        el = fromstring('<em>Text</em>')
        correct_response = '*Text*'
        response = self.t.translate(el)
        err_msg = 'Emphases are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_h_translators(self):
        print "Testing header translators"
        # Loop through <h[1:6]>
        for i in xrange(1, 7):
            print "\tTesting 'h" + `i` + "' translator...",
            el = fromstring('<h' + `i` + '>Heading</h' + `i` + '>')
            correct_response = ('#' * i) + 'Heading' + ('#' * i)
            response = self.t.translate(el)
            err_msg = 'Level ' + `i` + ' headings are not translating correctly\n'\
                        'Expected:\n' + correct_response + '\n---\n'\
                        'Recieved:\n' + response + "\n---"
            self.assertEqual(response, correct_response, err_msg)
            print "OK"
    def test_i_translator(self):
        print "Testing 'i' translator...",
        el = fromstring('<i>Text</i>')
        correct_response = '*Text*'
        response = self.t.translate(el)
        err_msg = 'Italics are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_img_translator(self):
        print "Testing 'img' translator...",
        el = fromstring('<img src="http://www.google.com/images/logos/logo.png" alt="Google!">')
        correct_response = '![Google!](http://www.google.com/images/logos/logo.png)'
        response = self.t.translate(el)
        err_msg = 'Images are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_li_translator(self):
        print "Testing 'li' translator...",
        el = fromstring('<li>List Text</li>')
        correct_response = 'List Text\n'
        response = self.t.translate(el)
        err_msg = 'List items are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_p_translator(self):
        print "Testing 'p' translator...",
        el = fromstring('<p>Text!</p>')
        correct_response = 'Text!\n\n'
        response = self.t.translate(el)
        err_msg = 'Paragraphs are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_pre_translator(self):
        print "Testing 'pre' translator...",
        el = fromstring('<pre>This is\nsome preformated\ntext</pre>')
        correct_response = 'This is some preformated text\n\n'
        response = self.t.translate(el)
        err_msg = 'Preformated text is not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_span_translator(self):
        print "Testing 'span' translator...",
        el = fromstring('<span>Text</span>')
        correct_response = 'Text'
        response = self.t.translate(el)
        err_msg = 'Spans are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"
    def test_strong_translator(self):
        print "Testing 'strong' translator...",
        el = fromstring('<strong>Text</strong>')
        correct_response = '**Text**'
        response = self.t.translate(el)
        err_msg = 'Strongs are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"

    def test_ul_translator(self):
        print "Testing 'ul' translator",
        el = fromstring('<ul><li>This is</li>\n<li>a list</li><li>of elements</li></ul>')
        correct_response = ' * This is\n * a list\n * of elements\n\n'
        response = self.t.translate(el)
        err_msg = 'Unordered lists are not translating correctly\n'\
                    'Expected:\n' + correct_response + '\n---\n'\
                    'Recieved:\n' + response + "\n---"
        self.assertEqual(response, correct_response, err_msg)
        print "OK"

    def test_files(self):
        import os, re
        cases = os.listdir(self.samples_dir)
        for case in cases:
            parts = re.search('(.+)\.(.+)', case)
            if parts.group(2) == 'md': continue
            case_name = parts.group(1)
            
            case_name_html = self.samples_dir + case_name + '.html'
            f_html = open(case_name_html, 'r')
            case_html = f_html.read()
            f_html.close()
            
            case_name_md = self.samples_dir + case_name + '.md'
            f_md = open(case_name_md, 'r')
            case_md = f_md.read()
            f_md.close()

            err_msg = 'Translation of ' + case_name_html + ' does not match ' + case_name_md
            self.assertEqual(case_md, self.t.translate(fromstring(case_html)), err_msg)
        print "OK"

# Run Tests
if __name__ == '__main__':
    unittest.main()

            
