#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 21:24
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""


#from blessings import Terminal
import unittest
import sys, re
import time
import datetime
import settings
import StringIO
from xml.sax import saxutils
import smtplib, mimetypes
from email.Header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class TerminalController:
    """Self Terminal"""
    # Background colors:
    BG_BLACK = BG_BLUE = BG_GREEN = BG_CYAN = ''
    BG_RED = BG_MAGENTA = BG_YELLOW = BG_WHITE = ''

    # Foreground colors:
    BLACK = BLUE = GREEN = CYAN = RED = MAGENTA = YELLOW = WHITE = ''

    # Terminal size:
    COLS = None          #: Width of the terminal (None for unknown)
    LINES = None         #: Height of the terminal (None for unknown)

    # Cursor display:
    HIDE_CURSOR = ''     #: Make the cursor invisible
    SHOW_CURSOR = ''     #: Make the cursor visible

    # Output modes:
    BOLD = ''            #: Turn on bold modern
    BLINK = ''           #: Turn on blink modern
    DIM = ''             #: Turn on half-bright modern
    REVERSE = ''         #: Turn on reverse-video modern
    NORMAL = ''          #: Turn off all modes

    # Deletion:
    CLEAR_SCREEN = ''    #: Clear the screen and move to home position
    CLEAR_EOL = ''       #: Clear to the end of the line.
    CLEAR_BOL = ''       #: Clear to the beginning of the line.
    CLEAR_EOS = ''       #: Clear to the end of the screen

    # Cursor movement:
    BOL = ''             #: Move the cursor to the beginning of the line
    UP = ''              #: Move the cursor up one line
    DOWN = ''            #: Move the cursor down one line
    LEFT = ''            #: Move the cursor left one char
    RIGHT = ''           #: Move the cursor right one char

    _STRING_CAPABILITIES = ""
    _COLORS = """BLACK BLUE GREEN CYAN RED MAGENTA YELLOW WHITE""".split()
    _ANSICOLORS = "BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE".split()
    def __init__(self, term_stream=sys.stdout):
        try:
            import curses
        except:
            return
        # If the stream isn't a tty, then assume it has no capabilities.
        if not term_stream.isatty():
            return

        # Check the terminal type.  If we fail, then assume that
        # the terminal has no capabilities.
        try:
            curses.setupterm()
        except:
            return

        # Look up numeric capabilities.
        self.COLS = curses.tigetnum('cols')
        self.LINES = curses.tigetnum('lines')
        # Look up string capabilities
        for capability in self._STRING_CAPABILITIES:
            (attrib, cap_name) = capability.split('=')
            setattr(self, attrib, self._tigetstr(cap_name) or '')
        # Colors
        set_fg = self._tigetstr('setf')
        if set_fg:
            for i, color in zip(range(len(self._COLORS)), self._COLORS):
                setattr(self, color, curses.tparm(set_fg, i) or '')
        set_fg_ansi = self._tigetstr('setaf')
        if set_fg_ansi:
            for i, color in zip(range(len(self._ANSICOLORS)), self._ANSICOLORS):
                setattr(self, color, curses.tparm(set_fg_ansi, i) or '')
        set_bg = self._tigetstr('setb')
        if set_bg:
            for i, color in zip(range(len(self._COLORS)), self._COLORS):
                setattr(self, 'BG_'+color, curses.tparm(set_bg, i) or '')
        set_bg_ansi = self._tigetstr('setab')
        if set_bg_ansi:
            for i, color in zip(range(len(self._ANSICOLORS)), self._ANSICOLORS):
                setattr(self, 'BG_'+color, curses.tparm(set_bg_ansi, i) or '')

    def _tigetstr(self, cap_name):
        # String capabilities can include "delays" of the form "$<2>".
        # For any modern terminal, we should be able to just ignore
        # these, so strip them out.
        import curses
        cap = curses.tigetstr(cap_name) or ''
        return re.sub(r'\$<\d+>[/*]?', '', cap)

    def render(self, template):
        """
        Replace each $-substitutions in the given template string with the
        corresponding terminal control string (if it's defined) or''
        (if it's not).
        """
        return re.sub(r'\$\$|\${\w+}', self._render_sub, template)

    def _render_sub(self, match):
        """Need Add docstring"""
        s = match.group()
        if s == '$$':
            return s
        else:
            return getattr(self, s[2:-1])


class MColorStream:
#class MColorStream(object):
    """Color Setting"""
    #def __init__(self):
    def __init__(self, stream):
        self.term = TerminalController()
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getattr__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def writeln(self, msg=None):
        term = self.term.render('${BOLD}${WHITE}%s${NORMAL}')
        if msg:
            self.write(term % msg)
        self.write(term % '\n')

    #print term.render('${YELLOW}Warning:${NORMAL}'), 'paper is crinkled'
    def red(self, msg):
        #self.write(self.term.red + self.term.bold + msg + self.term.normal)
        term = self.term.render('${BOLD}${RED}%s${NORMAL}')
        self.write(term % msg)

    def green(self, msg):
        #self.write(self.term.green + self.term.bold + msg + self.term.normal)
        term = self.term.render('${BOLD}${GREEN}%s${NORMAL}')
        self.write(term % msg)

    def yellow(self, msg):
        #self.write(self.term.yellow + self.term.bold + msg + self.term.normal)
        term = self.term.render('${BOLD}${YELLOW}%s${NORMAL}')
        self.write(term % msg)

    def cyan(self, msg):
        #self.write(self.term.cyan + self.term.bold + msg + self.term.normal)
        term = self.term.render('${BOLD}${CYAN}%s${NORMAL}')
        self.write(term % msg)

    def white(self, msg):
        #self.write(self.term.white + self.term.bold + msg + self.term.normal)
        term = self.term.render('${BOLD}${WHITE}%s${NORMAL}')
        self.write(term % msg)

    def blue(self, msg):
        #self.write(self.term.blue + self.term.bold + msg + self.term.normal)
        term = self.term.render('${BOLD}${WHITE}%s${NORMAL}')
        self.write(term % msg)


class MTextTestResult(unittest.TestResult):
    """Test Runner"""
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, description, verbosity):
        super(MTextTestResult, self).__init__()
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.description = description
        if settings.NeedLog:
            self.success_count = 0
            self.failure_count = 0
            self.error_count = 0
            self.stdout0 = sys.stdout
            self.stderr0 = sys.stderr
            self.result = []

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.description and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()
        if settings.NeedLog:
            self.outputBuffer = StringIO.StringIO()
            stdout_redirector.fp = self.outputBuffer
            stderr_redirector.fp = self.outputBuffer
            self.stdout0 = sys.stdout
            self.stderr0 = sys.stderr
            sys.stdout = stdout_redirector
            sys.stderr = stderr_redirector
        else:
            self.stream.writeln(self.separator1)
            self.stream.cyan('[Run\t]')
            self.stream.writeln(self.getDescription(test))

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def addSuccess(self, test):
        super(MTextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            if settings.NeedLog:
                self.success_count += 1
                output = self.complete_output()
                self.result.append((0, test, output, ''))
            else:
                self.stream.green('[OK\t]')
                self.stream.writeln(self.getDescription(test))
                self.stream.flush()

    def addError(self, test, err):
        super(MTextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            if settings.NeedLog:
                self.error_count += 1
                _, _exc_str = self.errors[-1]
                output = self.complete_output()
                self.result.append((2, test, output, _exc_str))
            else:
                self.stream.yellow('[ERROR\t]')
                self.stream.writeln(self.getDescription(test))
                self.stream.write(self._exc_info_to_string(err, test))
                self.stream.flush()

    def addFailure(self, test, err):
        super(MTextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            if settings.NeedLog:
                self.failure_count += 1
                _, _exc_str = self.failures[-1]
                output = self.complete_output()
                self.result.append((1, test, output, _exc_str))
            else:
                self.stream.red('[FAIL\t]')
                self.stream.writeln(self.getDescription(test))
                self.stream.write(self._exc_info_to_string(err, test))
                self.stream.flush()

class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.__fp = fp
    def write(self, s):
        self.fp.write(s)
    def writelines(self, lines):
        self.fp.writelines(lines)
    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

class Template_mixin(object):
    STATUS = {\
            0: 'pass', \
            1: 'fail', \
            2: 'error', \
            }
    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>%(title)s</title>
        <meta name="generator" content="%(generator)s"/>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
               %(stylesheet)s
    </head>
    <body>
      <script language="javascript" type="text/javascript">
      <!--output_list = Array();

function showCase(level) {
trs = document.getElementsByTagName("tr");
for (var i = 0; i < trs.length; i++) {
  tr = trs[i];
  id = tr.id;
  if (id.substr(0,2) == 'ft') {
   if (level < 1) {
    tr.className = 'hiddenRow';
   }
   else {
    tr.className = '';
   }
  }
  if (id.substr(0,2) == 'pt') {
    if (level > 1) {
      tr.className = '';
    }
    else {
     tr.className = 'hiddenRow';
    }
  }
}
}
function showClassDetail(cid, count) {
var id_list = Array(count);
var toHide = 1;
for (var i = 0; i < count; i++) {
 tid0 = 't' + cid.substr(1) + '.' + (i+1);
 tid = 'f' + tid0;
 tr = document.getElementById(tid);
 if (!tr) {
  tid = 'p' + tid0;
  tr = document.getElementById(tid);
 }
 id_list[i] = tid;
 if (tr.className) {
  toHide = 0;
 }
}
for (var i = 0; i < count; i++) {
 tid = id_list[i];
 if (toHide) {
  document.getElementById(tid).className = 'hiddenRow';
 }
 else {
  document.getElementById(tid).className = '';
 }
}
}

function showTestDetail(div_id){
var details_div = document.getElementById(div_id)
var displayState = details_div.style.display
// alert(displayState)
if (displayState != 'block' ) {
 displayState = 'block'
 details_div.style.display = 'block'
}
else {
details_div.style.display = 'none'
}
}

function html_escape(s) {
s = s.replace(/&/g,'&amp;');
s = s.replace(/</g,'&lt;');
s = s.replace(/>/g,'&gt;');
return s;
}
--></script>

%(heading)s
%(report)s
%(ending)s

</body>
</html>
"""
# variables: (title, generator, stylesheet, heading, report, ending)
# ------------------------------------------------------------------------
# Stylesheet
#
# alternatively use a <link> for external style sheet, e.g.
#   <link rel="stylesheet" href="$url" type="text/css">
    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
table       { font-size: 100%; }
pre         { }
h1 {
font-size: 16pt;
color: gray;
}
.heading {
margin-top: 0ex;
margin-bottom: 1ex;
}

.heading .attribute {
margin-top: 1ex;
margin-bottom: 0;
}

.heading .description {
margin-top: 4ex;
margin-bottom: 6ex;
}

/* -- css div popup ------------------------------------------------------------------------ */
a.popup_link {
}

a.popup_link:hover {
color: red;
}

.popup_window {
display: block;
position: relative;
left: 0px;
top: 0px;
/*border: solid #627173 1px; */
padding: 10px;
background-color: #E6E6D6;
font-family: "Lucida Console", "Courier New", Courier, monospace;
text-align: left;
font-size: 8pt;
width: 500px;
}

}
/* -- report ------------------------------------------------------------------------ */
#show_detail_line {
margin-top: 3ex;
margin-bottom: 1ex;
}
#result_table {
width: 80%;
border-collapse: collapse;
border: 1px solid #777;
}
#header_row {
font-weight: bold;
color: white;
background-color: #777;
}
#result_table td {
border: 1px solid #777;
padding: 2px;
}
#total_row  { font-weight: bold; }
.passClass  { background-color: #6c6; }
.failClass  { background-color: #c60; }
.errorClass { background-color: #c00; }
.passCase   { color: #6c6; }
.failCase   { color: #c60; font-weight: bold; }
.errorCase  { color: #c00; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
/* -- ending ---------------------------------------------------------------------- */
#ending {
}

</style>
"""
# ------------------------------------------------------------------------
# Heading
#
    HEADING_TMPL = """<div class='heading'>
<h1>%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>

""" # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
""" # variables: (name, value)
# ------------------------------------------------------------------------
# Report
#
    REPORT_TMPL = """
<p id='show_detail_line'>Show
<a href='javascript:showCase(0)'>Summary</a>
<a href='javascript:showCase(1)'>Failed</a>
<a href='javascript:showCase(2)'>All</a>
</p>
<table id='result_table'>
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
<td>Test Group/Test case</td>
<td>Count</td>
<td>Pass</td>
<td>Fail</td>
<td>Error</td>
<td>View</td>
</tr>
%(test_list)s
<tr id='total_row'>
<td>Total</td>
<td>%(count)s</td>
<td>%(Pass)s</td>
<td>%(fail)s</td>
<td>%(error)s</td>
<td>&nbsp;</td>
</tr>
</table>
""" # variables: (test_list, count, Pass, fail, error)
    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
<td>%(desc)s</td>
<td>%(count)s</td>
<td>%(Pass)s</td>
<td>%(fail)s</td>
<td>%(error)s</td>
<td><a href="javascript:showClassDetail('%(cid)s',%(count)s)">Detail</a></td>
</tr>
""" # variables: (style, desc, count, Pass, fail, error, cid)


    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
<td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
<td colspan='5' align='center'>

<!--css div popup start-->
<a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
%(status)s</a>

<div id='div_%(tid)s' class="popup_window">
<div style='text-align: right; color:red;cursor:pointer'>
<a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
[x]</a>
</div>
<pre>
%(script)s
</pre>
</div>
<!--css div popup end-->

</td>
</tr>
""" # variables: (tid, Class, style, desc, status)


    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
<td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
<td colspan='5' align='center'>%(status)s</td>
</tr>
""" # variables: (tid, Class, style, desc, status)


    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
""" # variables: (id, output)
# ------------------------------------------------------------------------
# ENDING
#

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""

# -------------------- The end of the Template class -------------------


class TextTestRunner(Template_mixin):
    resultclass = MTextTestResult

    def __init__(self, stream=sys.stderr, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None, title=None, description =None):
        self.stream = MColorStream(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        if resultclass is not None:
            self.resultclass = resultclass
        if settings.NeedLog:
            if title is None:
                self.title = self.DEFAULT_TITLE
            else:
                self.title = title
            if description is None:
                self.description = self.DEFAULT_DESCRIPTION
            else:
                self.description = description
            self.startTime = datetime.datetime.now()

    def _makeResult(self):
        """Need Add docstring"""
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        unittest.registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2') and not settings.NeedLog:
            self.stream.writeln(result.separator2)
        run = result.testsRun
        if not settings.NeedLog:
            self.stream.writeln("Ran %d test%s in %.3fs" %
                                (run, run != 1 and "s" or "", timeTaken))
            self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            if not settings.NeedLog:
                self.stream.write("FAILED")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("error=%d" % errored)
        else:
            if not settings.NeedLog:
                self.stream.write("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos and not settings.NeedLog:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            if not settings.NeedLog:
                self.stream.write("\n")
        if settings.NeedLog:
            self.stopTime = datetime.datetime.now()
            self.generateReport(test, result)
        return result
    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n,t,o,e in result_list:
            cls = t.__class__
            if not rmap.has_key(cls):
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n,t,o,e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        status.append('Total Run %s'   % (result.success_count + result.failure_count + result.error_count))
        if result.success_count:
            status.append('Pass %s'    % result.success_count)
        if result.failure_count:
            status.append('Failure %s' % result.failure_count)
        if result.error_count:
            status.append('Error %s'   % result.error_count  )
        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [('Start Time', startTime),('Duration', duration),('Status', status),]
    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner'
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(title = saxutils.escape(self.title),generator = generator,\
                                       stylesheet = stylesheet,heading = heading,report = report,ending = ending,)
        self.stream.write(output.encode('utf8'))
        self.send_email_with_html(settings.MAIL_RECEIVE, output, "Unit Test Repor %s"%datetime.date.today())

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(name = saxutils.escape(name),\
                                                      value = saxutils.escape(value),)
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(title = saxutils.escape(self.title),parameters = ''.join(a_lines),\
                                           description = saxutils.escape(self.description),)
        return heading

    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            for n,t,o,e in cls_results:
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                else: ne += 1
            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name
            row = self.REPORT_CLASS_TMPL % dict(style = ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',\
                                                desc = desc,count = np+nf+ne,Pass = np,fail = nf,error = ne,cid = 'c%s' % (cid+1),)
            rows.append(row)
            for tid, (n,t,o,e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)
            
        report = self.REPORT_TMPL % dict(
            test_list = ''.join(rows),
            count = str(result.success_count+result.failure_count+result.error_count),
            Pass = str(result.success_count),
            fail = str(result.failure_count),
            error = str(result.error_count),)
        return report

    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid+1,tid+1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(o,str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            uo = o.decode('latin-1')
        else:
            uo = o
        if isinstance(e,str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            ue = e.decode('latin-1')
        else:
            ue = e
        
        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id = tid,
            output = saxutils.escape(uo+ue),
        )
        
        row = tmpl % dict(
            tid = tid,
            Class = (n == 0 and 'hiddenRow' or 'none'),
            style = n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'none'),
            desc = desc,
            script = script,
            status = self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL
    def send_email_with_html(self, addressee, html, subject):
        """发送html email"""
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = settings.DIRECTOR['EMAIL']
        to_list = [ str(adr).strip() for adr in addressee.split(';')] if type(addressee) in [str,type(u'')] else addressee
        msg['To'] = ';'.join(to_list) 
        html_att = MIMEText(html, 'html', 'utf-8')
        msg.attach(html_att)
        
        try:
            smtp = smtplib.SMTP()
            smtp.connect(settings.DIRECTOR['sendserverip'], settings.DIRECTOR['sendserverport']) 
            smtp.login(msg['From'], settings.DIRECTOR['SECRET'])
            smtp.sendmail(msg['From'], to_list, msg.as_string())
        except Exception,e:
            print e

