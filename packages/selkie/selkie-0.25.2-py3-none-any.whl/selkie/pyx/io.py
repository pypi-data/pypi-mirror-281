'''
The io module contains input and output streams.
'''

try:
    from fcntl import flock, LOCK_EX, LOCK_UN
except:
    flock = LOCK_EX = LOCK_UN = None

import sys, os, urllib, urllib.request, urllib.parse, urllib.error, \
    codecs, shutil, subprocess, stat, threading, datetime, random, \
    json
from glob import glob
from io import StringIO, TextIOBase
from os.path import exists
from pathlib import Path
from collections import namedtuple
from .seq import as_list
from .string import as_ascii
from .xterm import fg


def ispathlike (x):
    return isinstance(x, str) or hasattr(x, '__fspath__')


#--  Suffixes  -----------------------------------------------------------------

##  A suffix begins with the final period, provided that it occurs in the final
#   pathname component.  Returns the pathname sans suffix.

def strip_suffix (fn):
    i = fn.rfind('.')
    if i > 0 and '/' not in fn[i+1:]:
        return fn[:i]
    else:
        return fn

##  Returns a pair: (filename sans suffix, suffix sans period).

def split_suffix (fn):
    i = fn.rfind('.')
    if i > 0 and '/' not in fn[i+1:]:
        return (fn[:i], fn[i+1:])
    else:
        return (fn, '')

##  Returns the suffix or an empty string.  The period is not included.

def get_suffix (fn):
    i = fn.rfind('.')
    if i > 0 and '/' not in fn[i+1:]:
        return fn[i+1:]
    else:
        return ''


#--  Contents  -----------------------------------------------------------------

def contents (filename, encoding=None):
    with open(filename, encoding=encoding) as f:
        return f.read()


#--  Tokens  -------------------------------------------------------------------

##  A token.

class Token (str):

    ##  True if type is 'any' or equals the token's type.
    def hastype (self, type):
        if type == 'any': return self.type != 'eof'
        else: return type == self.type

    ##  Raise an exception, indicating file, line, and offset.
    def error (self, msg='syntax error'):
        raise Exception('[%s line %d char %d] %s' % \
            (self.filename, self.line, self.offset, msg))

    ##  Print a warning, indicating file, line, and offset.
    def warn (self, msg):
        sys.stderr.write('WARNING: [%s line %d char %d] %s\n' % \
                             (self.filename, self.line, self.offset, msg))


##  Represents the syntax of a little language.

class Syntax (object):

    QuoteChars = '"\''
    DefaultSpecialChars = '()[]{}'

    def __init__ (self,
                  special=None,
                  eol=False,
                  comments=True,
                  multi=None,
                  backslash=True,
                  stringtype='word',
                  mlstrings=False,
                  digits=False):

        ##  The special characters.  True means everything except alphanumerics
        #   and whitespace.
        self.special = self.DefaultSpecialChars if special is None else special

        ##  Multi-character sequences that should be recognized as tokens.
        self.multi = None

        ##  The start characters for multi-character sequences.
        self.multi_start = None

        ##  Whether to include newline as a token.
        self.eol = eol

        ##  What character/string introduces comments.  Default: '#'.
        self.comments = None

        ##  Whether to interpret backslash as escape.
        self.backslash = backslash

        ##  What token type to use for a quoted string.  Default: 'word'.
        self.stringtype = stringtype

        ##  Whether to permit strings to extend over multiple lines.  Default: False.
        self.mlstrings = mlstrings

        ##  Whether to return digit sequences as tokens.
        self.digits = digits


        if comments is True:
            self.comments = '#'
        elif not comments:
            self.comments = ''

        if special is True:
            # everything is special except alphanum and underscore
            self.special = True
        else:
            self.special = (special or '') + self.QuoteChars + self.comments

        self.multi = multi
        if multi:
            self.multi = sorted(multi, key=len, reverse=True)
            self.multi_start = ''.join(set(s[0] for s in multi))
        else:
            self.multi_start = ''

    ##  Convert s to a string that will scan correctly.

    def scanable_string (self, s):
        if not isinstance(s, str):
            s = str(s)
        for c in s:
            if c.isspace() or c in self.special:
                s = repr(s)
                if s[0] == 'u': return s[1:]
                else: return s
        return s

    ##  String representation.

    def __repr__ (self):
        return '<Syntax %s %s>' % (self.special, self.eol)

    
    ##  Tokenize a file, returning a list.
    
    def load_tokens (self, filename, encoding=None):
        return list(self.iter_tokens(filename, encoding))
    
    ##  Iterate over tokens of a string.
    
    def tokenize (self, s, encoding=None):
        return self.iter_tokens(StringIO(s), encoding)
    
    ##  Iterator over tokens.
    
    def iter_tokens (self, filename, encoding=None):
        return self.TokenIterator(self, filename, encoding)

    class TokenIterator (object):
    
        ##  Constructor.
    
        def __init__ (self, syntax, filename, encoding):
    
            ##  A Syntax instance.
            self.syntax = syntax
    
            ##  Stack, for (possibly nested) temporary syntax changes.
            self.stack = []
    
            ##  Filename string; set even for streams not associated with files.
            self.filename = filename_string(filename)
    
            ##  The lines of the file.
            self.lines = load_lines(filename, encoding)  # no newlines in lines
    
            ##  The current line.
            self.line = None
    
            ##  Current line number.
            self.linecount = 1
    
            ##  Current character offset on the line.
            self.offset = 0
    
            ##  Previous linecount.
            self.old_linecount = 1
    
            ##  Previous offset.
            self.old_offset = 0
    
            self.__token = None
    
            if self.lines: self.line = self.lines[0]
            else: self.line = ''
    
        ##  Returns self.
    
        def __iter__ (self):
            return self
    
        ##  Whether we are at EOF.
    
        def __bool__ (self):
            return self.token().type != 'eof'
    
        def __readline (self):
            if self.linecount < len(self.lines):
                self.line = self.lines[self.linecount]
                self.linecount += 1
            elif self.linecount == len(self.lines):
                self.line = ''
                self.linecount += 1
            else:
                raise Exception('Readline after EOF')
            self.offset = 0
    
        def __at_eof (self):
            return self.linecount > len(self.lines)
    
        def __empty_line (self):
            for c in self.line:
                if c in self.syntax.comments: return True
                elif not c.isspace(): return False
            return True
    
        def __is_special (self, c):
            if self.syntax.special is True:
                return not (c.isalnum() or c == '_')
            else:
                return c in self.syntax.special
    
        ##  Advance, if necessary, then return the current token.
    
        def token (self):
            if self.__token is None: self.__advance()
            return self.__token
    
        def __skip_eol (self):
            if self.offset >= len(self.line):
                if self.syntax.eol and not self.__empty_line():
                    self.__set_token('\n', self.offset, string='\n')
                    self.__readline()
                else:
                    while self.offset >= len(self.line):
                        if self.__at_eof():
                            self.__set_token('eof', self.offset)
                            break
                        self.__readline()
    
        def __advance (self):
            self.old_linecount = self.linecount
            self.old_offset = self.offset
            self.__token = None
            try:
                while self.__token is None:
                    self.__skip_eol()
                    if self.__token is not None: return
                    c = self.line[self.offset]
    
                    if c in self.syntax.multi_start and self.__scan_multi(): pass
                    elif c in self.syntax.comments: self.offset = len(self.line)
                    elif c == "'" or c == '"': self.__scan_quoted()
                    elif c.isspace(): self.offset += 1
                    elif self.__is_special(c): self.__scan_special()
                    elif self.syntax.digits and self.__is_digit(c): self.__scan_digit()
                    else: self.__scan_word()
    
            except StopIteration:
                raise Exception('[%s line %d offset %d] Unexpected eof' % \
                    (self.filename, self.linecount, self.offset))
    
        def __retreat (self):
            self.__token = None
            self.linecount = self.old_linecount
            self.offset = self.old_offset
            if self.linecount > 0:
                self.line = self.lines[self.linecount-1]
            else:
                self.line = None
    
        def __set_token (self, type, start, line=None, string=None, quotes=None):
            if line is None:
                line = self.linecount
            if string is None:
                string = self.line[start:self.offset]
            self.__token = Token(string)
            self.__token.type = type
            self.__token.filename = self.filename
            self.__token.line = line
            self.__token.offset = start
            self.__token.quotes = quotes
    
        def __is_digit (self, c):
            if c.isdigit(): return True
            i = self.offset + 1
            return c == '-' and i < len(self.line) and self.line[i].isdigit()
    
        def __scan_digit (self):
            start = self.offset
            if self.line[self.offset] == '-': self.offset += 1
            while self.offset < len(self.line) and self.line[self.offset].isdigit():
                self.offset += 1
            self.__set_token('digit', start)
    
        def __scan_word (self):
            start = self.offset
            while self.offset < len(self.line):
                c = self.line[self.offset]
                if c.isspace() or self.__is_special(c): break
                self.offset += 1
            self.__set_token('word', start)
    
        def __error (self, start, msg):
            raise Exception('[%s line %d char %d] %s' % \
                (self.filename, self.linecount, start, msg))
    
        def __scan_quoted (self):
            delim = self.line[self.offset]
            self.offset += 1
            start = self.offset
            restart = self.offset
            frags = []
            while True:
                while self.offset >= len(self.line):
                    if self.syntax.mlstrings:
                        if restart < len(self.line):
                            frags.append(self.line[restart:])
                        frags.append('\n')
                        self.__readline()
                        restart = self.offset
                        if self.__at_eof():
                            self.__error(start, 'Unterminated string at EOF')
                    else:
                        self.__error(start, 'End of line in string')
                c = self.line[self.offset]
                if c == delim:
                    frags.append(self.line[restart:self.offset])
                    self.offset += 1
                    break
                elif c == '\\' and self.syntax.backslash:
                    frags.append(self.line[restart:self.offset])
                    frags.append(self.__scan_escape_sequence())
                    restart = self.offset
                else:
                    self.offset += 1
            self.__set_token(self.syntax.stringtype, start, self.linecount, ''.join(frags), delim)
    
        def __scan_escape_sequence (self):
            # self.line[self.offset] is backslash
            self.offset += 1
            if self.offset >= len(self.line): self.__error('Bad escape sequence')
            c = self.line[self.offset]
            self.offset += 1
            if c == '\\' or c == '"' or c == "'": return c
            elif c == 'a': return '\a'
            elif c == 'b': return '\b'
            elif c == 'f': return '\f'
            elif c == 'n': return '\n'
            elif c == 'r': return '\r'
            elif c == 't': return '\t'
            elif c == 'u':
                i = self.offset
                self.offset += 4
                if self.offset > len(self.line): self.__error('Bad escape sequence')
                return chr(int(self.line[i:self.offset], 16))
            elif c == 'U':
                self.__error('\\U escapes not implemented')
            elif c == 'v': return '\v'
            elif '0' <= c <= '7':
                i = self.offset
                self.offset += 1
                n = 1
                while n < 3 and self.offset < len(self.line) and \
                        '0' <= self.line[self.offset] <= '7':
                    self.offset += 1
                    n += 1
                return chr(int(self.line[i:self.offset], 8))
            elif c == 'x':
                i = self.offset
                self.offset += 1
                if self.offset < len(self.line) and \
                        ('0' <= self.line[self.offset] <= '9' or \
                         'a' <= self.line[self.offset] <= 'f' or \
                         'A' <= self.line[self.offset] <= 'F'):
                    self.offset += 1
                d = int(self.line[i:self.offset], 16)
                if d < 0x100: return chr(d)
                else: return chr(d)
    
        def __scan_special (self):
            start = self.offset
            self.offset += 1
            self.__set_token(self.line[start], start)
    
        def __looking_at (self, word):
            for i in range(len(word)):
                t = self.offset + i
                if t >= len(self.line): return False
                if self.line[t] != word[i]: return False
            return True
    
        def __scan_multi (self):
            for word in self.syntax.multi:
                if self.__looking_at(word):
                    start = self.offset
                    self.offset += len(word)
                    self.__set_token(self.line[start:self.offset], start)
                    return True
    
        ##  Whether the next token is something other than EOF.
        #   If type or string is provided, the value indicates whether the next
        #   token has the given type and/or string.
    
        def has_next (self, type=None, string=None):
            if string:
                if type: raise Exception("Provide only one argument")
                return self.token() == string
            elif type:
                return self.token().hastype(type)
            else:
                return self.token().type != 'eof'
    
        ##  Iterator method.
    
        def __next__ (self):
            token = self.token()
            if token.type == 'eof': raise StopIteration
            self.__token = None
            self.old_linecount = self.linecount
            self.old_offset = self.offset
            return token
    
        ##  If the next token matches the given type and/or string, return it
        #   and advance.  Otherwise, return None.
    
        def accept (self, type=None, string=None):
            token = self.token()
            if type and not token.hastype(type):
                return None
            if string and not (token == string):
                return None
            return next(self)
    
        ##  If the next token has the given type and/or string, return it
        #   and advance.  Otherwise, signal an error.  Returns None at EOF.
    
        def require (self, type=None, string=None):
            token = self.token()
            if type and not token.hastype(type):
                token.error('Expecting ' + repr(type))
            if string and not (token == string):
                token.error('Expecting ' + repr(string))
            if type == 'eof': return None
            else: return next(self)
    
        ##  Signal an error, indicating filename and line number.
    
        def error (self, msg=None):
            token = self.token()
            token.error(msg)
    
        ##  Print a warning, showing filename and line number.
    
        def warn (self, msg=None):
            token = self.token()
            token.warn(msg)
    
        ##  Push the current syntax on the stack and switch to the given syntax.
    
        def push_syntax (self, syntax):
            self.stack.append(self.syntax)
            self.syntax = syntax
            self.__retreat()
    
        ##  Restore the previous syntax from the stack.
    
        def pop_syntax (self):
            if not self.stack: raise Exception('Empty stack')
            self.syntax = self.stack.pop()
            self.__retreat()


DefaultSyntax = Syntax()


#--  pprint  -------------------------------------------------------------------

##  A PPrinter instance.
pprint = None


##  Indentation for a PPrinter.

class PPrintIndent (object):

    ##  Constructor.

    def __init__ (self, pprinter, n):

        ##  The pprinter.
        self.pprinter = pprinter

        ##  The number of spaces indented by.
        self.n = n

    ##  Enter.

    def __enter__ (self):
        self.pprinter._indent += self.n

    ##  Exit.

    def __exit__ (self, t, v, tb):
        self.pprinter._indent -= self.n
        

##  A color for a PPrinter.

class PPrintColor (object):

    ##  Constructor.

    def __init__ (self, pprinter, color):

        ##  The pprinter.
        self.pprinter = pprinter

        ##  The color.
        self.color = color

        ##  Saves the previous color.
        self.prevcolor = None

    def _set_color (self, color):
        self.pprinter._color = color
        sys.stdout.write(fg[color])
        sys.stdout.flush()

    ##  Enter.

    def __enter__ (self):
        self.prevcolor = self.pprinter._color or 'default'
        self._set_color(self.color)

    ##  Exit.

    def __exit__ (self, t, v, tb):
        self._set_color(self.prevcolor)


##  A pretty-printer.

class PPrinter (object):

    ##  Constructor.

    def __init__ (self, file=None):
        self._color = None
        self._indent = 0
        self._atbol = True
        self._brflag = False
        self._file = file
    
    ##  String representation.

    def __repr__ (self):
        return '<PPrinter %s>' % repr(self._file)

    ##  The protected file.

    def file (self):
        if self._file is None: return sys.stdout
        else: return self._file

    ##  Returns an indentation.  Calling this in a with-statement causes the
    #   indentation to be active within the body.

    def indent (self, n=2):
        return PPrintIndent(self, n)

    ##  Start an indentation.  One should usually do "with pp.indent()" instead.

    def start_indent (self, n=2):
        self._indent += n
    
    ##  End an indentation.

    def end_indent (self, n=2):
        self._indent -= n
        if self._indent < 0: self._indent = 0
    
    ##  Freshline.

    def br (self):
        self._brflag = True

    ##  Returns a color.  Calling this in a with-statement causes the color
    #   to be used in the body.

    def color (self, c):
        return PPrintColor(self, c)

    ##  Like print().  Handles embedded newlines correctly.

    def __call__ (self, *args, end=None, color=None):
        if color is None:
            self._call1(args, end)
        else:
            with self.color(color):
                self._call1(args, end)
                
    def _call1 (self, args, end):
        if end is None and (len(args) == 0 or not hasattr(args[-1], '__pprint__')):
            end = '\n'
        first = True
        for arg in args:
            if first: first = False
            else: self.file().write(' ')
            self._printarg(arg)
        if end:
            self._printarg(end)

    def _printarg (self, arg):
        if hasattr(arg, '__pprint__'):
            arg.__pprint__()
        else:
            self.write(str(arg))

    ##  Write a string.

    def write (self, s):
        f = self.file()
        i = 0
        n = len(s)
        while i < n:
            j = s.find('\n', i)
            if j < 0: j = n
            # it is possible that s[0] == '\n'
            if i < j:
                if self._brflag and not self._atbol:
                    f.write('\n')
                    self._atbol = True
                if self._atbol:
                    f.write(' ' * self._indent)
                f.write(s[i:j].replace('\x1b', '\\x1b'))
                self._atbol = False
            # if j < n then s[j] == '\n'
            if j < n:
                f.write('\n')
                j += 1
                self._atbol = True
            i = j
    
    ##  Emit a newline, unless the last character printed was a newline.

    def freshline (self):
        if not self._atbol:
            self.write('\n')

    ##  Print and immediately flush.

    def now (self, *args, end=''):
        self.__call__(*args, end)
        self.file().flush()
    
    ##  Flush the output.

    def flush (self):
        self.file().flush()


pprint = PPrinter()


#--  tabular  ------------------------------------------------------------------

def __getcell (row, j, tostring):
    if len(row) > j: return tostring(row[j])
    else: return ''

def __compute_width (rows, j, tostring):
    return max(len(__getcell(r,j,tostring)) for r in rows)

def colalign (rows, header=None, indent='', tostring=str, hlines=True):
    tmp = []
    if header: tmp.append(header)
    tmp.extend(rows)
    rows = tmp
    ncols = max(len(r) for r in rows)
    widths = [__compute_width(rows,j,tostring) for j in range(ncols)]
    for i in range(len(rows)):
        line = indent
        for j in range(ncols):
            if j: line += ' '
            line += '%-*s' % (widths[j], __getcell(rows[i], j, tostring))
        rows[i] = line
    if hlines:
        linewidth = sum(widths) + ncols - 1
        hline = '-' * linewidth
        if header:
            rows[1:1] = [hline]
        rows[-1:-1] = [hline]
    return rows

##  Produces a string representation of a table with aligned columns,
#   suitable for printing.

def tabular (rows, header=None, indent='', tostring=str, hlines=True):
    return '\n'.join(colalign(rows, header, indent, tostring, hlines))



#--  OutputRedirected  ---------------------------------------------------------

##  Does the actual output redirection.
class _Redirect (object):

    ##  Constructor.
    def __init__ (self):
        ##  The output file.
        self.output = None

    ##  Call it.
    def __call__ (self, f=None, mode=None):
        if f is None:
            return Redirection(StringIO(), True, self)
        elif mode:
            return Redirection(_open(f, mode), True)
        elif isinstance(f, str):
            mode = 'w'
            return Redirection(_open(f, mode), True)            
        else:
            return Redirection(f)


##  Output redirection.  One should not generally instantiate this class
#   directly.  Rather, use the redirect() function.

class Redirection (object):

    ##  Constructor.

    def __init__ (self, file, toclose=False, caller=None):

        ##  The file redirected to.
        self.file = file

        ##  Whether it should be closed when done.
        self.toclose = toclose

        ##  If caller is set, then caller.output gets set to file.getvalue() on exit.
        self.caller = caller

        ##  To save the old value of stdout.
        self.stdout = None

        ##  To save the old value of stderr.
        self.stderr = None

    ##  Enter.  Stdout and stderr are set to my file.

    def __enter__ (self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self.file
        sys.stderr = self.file
        return self

    ##  Exit.  If there is a caller, set caller.output to file.getvalue().
    #   If toclose is True, close the file.  Restore stdout and stderr.

    def __exit__ (self, etype, evalue, traceback):
        if self.caller is not None: self.caller.output = self.file.getvalue()
        if self.toclose: self.file.close()
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    ##  Write a string to the file.

    def write (self, s):
        self.file.write(s)

    ##  Flush the file.

    def flush (self):
        self.file.flush()


##  Returns a Redirection, for use in a with-statement.
#   Arguments: filename and mode.
#   Call it with no arguments to get redirection to a string.
#   For example:
#
#       with redirect() as f:
#           f.write(...)
#           out = f.output
#

redirect = _Redirect()


#--  BackingSave  --------------------------------------------------------------

##  Handles locking (only).

class BackingAdmin (object):

    ##  Constructor.

    def __init__ (self, fn):

        ##  The filename.
        self.filename = fn

        ##  The lock, when locked.
        self.lock = None

    ##  Lock the file.

    def __enter__ (self):
        self.lock = open(fn + '.lock', 'w')
        flock(self.lock, LOCK_EX)
        return self

    ##  Release the lock.

    def __exit__ (self, type, value, tb):
        self.lock.close()
    
    ##  Replace the file with the backup version.

    def undo (self):
        bakfn = self.filename + '.bak'
        if not exists(bakfn):
            raise Exception('No undo information available: %s' % fn)
        if exists(self.filename):
            os.replace(self.filename, self.filename + '.redo')
        os.replace(bakfn, self.filename)

    ##  Restore the old version after an undo.

    def redo (self):
        redofn = self.filename + '.redo'
        if not exists(redofn):
            raise Exception('No redo information available')
        bakfn = self.filename + '.bak'
        if exists(self.filename):
            if exists(bakfn):
                os.unlink(bakfn)
            os.replace(self.filename, bakfn)
        os.replace(redofn, self.filename)


##  Handles backup and locking.

class BackingSave (object):

    ##  Constructor.

    def __init__ (self, fn, binary=False, makedirs=False):

        ##  Filename.
        self.filename = fn

        ##  The file.
        self.file = None

        ##  Whether to create missing directories.
        self.makedirs = makedirs

        ##  Whether it is a binary file.
        self.binary = binary

        ##  Write to a temp file, only touch the protected file if all writes
        #   complete successfully.
        self.tmp = fn + '.tmp'

        ##  The lock, while locked.
        self.lock = None

    ##  Enter.  Create any missing directories.  Lock the file.
    #   Open the temp file.  Return the temp file.

    def __enter__ (self):
        dir = os.path.dirname(self.filename)
        # if filename contains no slash, dir is ''
        if dir and not exists(dir):
            if self.makedirs:
                os.makedirs(dir)
            else:
                raise Exception('Directory does not exist: %s' % dir)
        self.lock = open(self.filename + '.lock', 'w')
        flock(self.lock, LOCK_EX)
        if self.binary: mode = 'wb'
        else: mode = 'w'
        self.file = open(self.tmp, mode)
        return self.file

    ##  Close the temp file.  If no error occurred, move the current
    #   file to backup and move the temp file into its place.
    #   If an error occurred, just delete the temp file.
    #   Release the lock.

    def __exit__ (self, type, value, traceback):
        self.file.close()
        if type is None:
            bak = self.filename + '.bak'
            if exists(bak):
                os.unlink(bak)
            if exists(self.filename):
                shutil.move(self.filename, bak)
            shutil.move(self.tmp, self.filename)
        else:
            if exists(self.tmp):
                os.unlink(self.tmp)
        self.lock.close()



# 
# class Cell (object):
# 
#     def __init__ (self, array, i=0):
#         if isinstance(array, BaseFile):
#             array = Array(array)
# 
#         self._array = array
#         self._i = i
# 
#     def get (self):
#         return self._array[self._i]
# 
#     def set(self, value):
#         self._array[self._i] = value
# 
#     def save (self):
#         self._array.save()
# 
#     def __enter__ (self):
#         return self
# 
#     def __exit__ (self, t, v, tb):
#         if not t:
#             self._array.save()
# 

# class SingletonFile (object):
# 
#     def load (self): raise NotImplementedError
#     def save (self, contents): raise NotImplementedError
# 
#     def __iter__ (self):
#         yield self.load()
# 
#     def store (self, contents):
#         self.save(contents)
# 
# 
# class LoadableFile (SingletonFile):
# 
#     def __init__ (self, fmt, f):
#         SingletonFile.__init__(self)
#         self._format = fmt
#         self._file = f
# 
#     def load (self):
#         return self._format.read(self._file)
# 
#     def save (self, contents):
#         self._file.store(self._format.render(contents))


#--  Tokens  -------------------------------------------------------------------

# class Tokenizer (object):
# 
#     ##  Constructor.  Filename only for printing error messages; need not be genuine filename.
# 
#     def __init__ (self, filename, lines, syntax=DefaultSyntax):
# 
#         ##  A Syntax instance.
#         self.syntax = syntax
# 
#         ##  Stack, for (possibly nested) temporary syntax changes.
#         self.stack = []
# 
#         ##  Filename string; set even for streams not associated with files.
#         self.filename = filename
# 
#         ##  The lines of the file.
#         self.lines = lines
# 
#         ##  The current line.
#         self.line = None
# 
#         ##  Current line number.
#         self.linecount = 1
# 
#         ##  Current character offset on the line.
#         self.offset = 0
# 
#         ##  Previous linecount.
#         self.old_linecount = 1
# 
#         ##  Previous offset.
#         self.old_offset = 0
# 
#         self.__token = None
# 
#         if self.lines: self.line = self.lines[0]
#         else: self.line = ''
# 
#     ##  Returns self.
# 
#     def __iter__ (self):
#         return self
# 
#     ##  Whether we are at EOF.
# 
#     def __bool__ (self):
#         return self.token().type != 'eof'
# 
#     def __readline (self):
#         if self.linecount < len(self.lines):
#             self.line = self.lines[self.linecount]
#             self.linecount += 1
#         elif self.linecount == len(self.lines):
#             self.line = ''
#             self.linecount += 1
#         else:
#             raise Exception('Readline after EOF')
#         self.offset = 0
# 
#     def __at_eof (self):
#         return self.linecount > len(self.lines)
# 
#     def __empty_line (self):
#         for c in self.line:
#             if c in self.syntax.comments: return True
#             elif not c.isspace(): return False
#         return True
# 
#     def __is_special (self, c):
#         if self.syntax.special is True:
#             return not (c.isalnum() or c == '_')
#         else:
#             return c in self.syntax.special
# 
#     ##  Advance, if necessary, then return the current token.
# 
#     def token (self):
#         if self.__token is None: self.__advance()
#         return self.__token
# 
#     def __skip_eol (self):
#         if self.offset >= len(self.line):
#             if self.syntax.eol and not self.__empty_line():
#                 self.__set_token('\n', self.offset, string='\n')
#                 self.__readline()
#             else:
#                 while self.offset >= len(self.line):
#                     if self.__at_eof():
#                         self.__set_token('eof', self.offset)
#                         break
#                     self.__readline()
# 
#     def __advance (self):
#         self.old_linecount = self.linecount
#         self.old_offset = self.offset
#         self.__token = None
#         try:
#             while self.__token is None:
#                 self.__skip_eol()
#                 if self.__token is not None: return
#                 c = self.line[self.offset]
# 
#                 if c in self.syntax.multi_start and self.__scan_multi(): pass
#                 elif c in self.syntax.comments: self.offset = len(self.line)
#                 elif c == "'" or c == '"': self.__scan_quoted()
#                 elif c.isspace(): self.offset += 1
#                 elif self.__is_special(c): self.__scan_special()
#                 elif self.syntax.digits and self.__is_digit(c): self.__scan_digit()
#                 else: self.__scan_word()
# 
#         except StopIteration:
#             raise Exception('[%s line %d offset %d] Unexpected eof' % \
#                 (self.filename, self.linecount, self.offset))
# 
#     def __retreat (self):
#         self.__token = None
#         self.linecount = self.old_linecount
#         self.offset = self.old_offset
#         if self.linecount > 0:
#             self.line = self.lines[self.linecount-1]
#         else:
#             self.line = None
# 
#     def __set_token (self, type, start, line=None, string=None, quotes=None):
#         if line is None:
#             line = self.linecount
#         if string is None:
#             string = self.line[start:self.offset]
#         self.__token = Token(string)
#         self.__token.type = type
#         self.__token.filename = self.filename
#         self.__token.line = line
#         self.__token.offset = start
#         self.__token.quotes = quotes
# 
#     def __is_digit (self, c):
#         if c.isdigit(): return True
#         i = self.offset + 1
#         return c == '-' and i < len(self.line) and self.line[i].isdigit()
# 
#     def __scan_digit (self):
#         start = self.offset
#         if self.line[self.offset] == '-': self.offset += 1
#         while self.offset < len(self.line) and self.line[self.offset].isdigit():
#             self.offset += 1
#         self.__set_token('digit', start)
# 
#     def __scan_word (self):
#         start = self.offset
#         while self.offset < len(self.line):
#             c = self.line[self.offset]
#             if c.isspace() or self.__is_special(c): break
#             self.offset += 1
#         self.__set_token('word', start)
# 
#     def __error (self, start, msg):
#         raise Exception('[%s line %d char %d] %s' % \
#             (self.filename, self.linecount, start, msg))
# 
#     def __scan_quoted (self):
#         delim = self.line[self.offset]
#         self.offset += 1
#         start = self.offset
#         restart = self.offset
#         frags = []
#         while True:
#             while self.offset >= len(self.line):
#                 if self.syntax.mlstrings:
#                     if restart < len(self.line):
#                         frags.append(self.line[restart:])
#                     frags.append('\n')
#                     self.__readline()
#                     restart = self.offset
#                     if self.__at_eof():
#                         self.__error(start, 'Unterminated string at EOF')
#                 else:
#                     self.__error(start, 'End of line in string')
#             c = self.line[self.offset]
#             if c == delim:
#                 frags.append(self.line[restart:self.offset])
#                 self.offset += 1
#                 break
#             elif c == '\\' and self.syntax.backslash:
#                 frags.append(self.line[restart:self.offset])
#                 frags.append(self.__scan_escape_sequence())
#                 restart = self.offset
#             else:
#                 self.offset += 1
#         self.__set_token(self.syntax.stringtype, start, self.linecount, ''.join(frags), delim)
# 
#     def __scan_escape_sequence (self):
#         # self.line[self.offset] is backslash
#         self.offset += 1
#         if self.offset >= len(self.line): self.__error('Bad escape sequence')
#         c = self.line[self.offset]
#         self.offset += 1
#         if c == '\\' or c == '"' or c == "'": return c
#         elif c == 'a': return '\a'
#         elif c == 'b': return '\b'
#         elif c == 'f': return '\f'
#         elif c == 'n': return '\n'
#         elif c == 'r': return '\r'
#         elif c == 't': return '\t'
#         elif c == 'u':
#             i = self.offset
#             self.offset += 4
#             if self.offset > len(self.line): self.__error('Bad escape sequence')
#             return chr(int(self.line[i:self.offset], 16))
#         elif c == 'U':
#             self.__error('\\U escapes not implemented')
#         elif c == 'v': return '\v'
#         elif '0' <= c <= '7':
#             i = self.offset
#             self.offset += 1
#             n = 1
#             while n < 3 and self.offset < len(self.line) and \
#                     '0' <= self.line[self.offset] <= '7':
#                 self.offset += 1
#                 n += 1
#             return chr(int(self.line[i:self.offset], 8))
#         elif c == 'x':
#             i = self.offset
#             self.offset += 1
#             if self.offset < len(self.line) and \
#                     ('0' <= self.line[self.offset] <= '9' or \
#                      'a' <= self.line[self.offset] <= 'f' or \
#                      'A' <= self.line[self.offset] <= 'F'):
#                 self.offset += 1
#             d = int(self.line[i:self.offset], 16)
#             if d < 0x100: return chr(d)
#             else: return chr(d)
# 
#     def __scan_special (self):
#         start = self.offset
#         self.offset += 1
#         self.__set_token(self.line[start], start)
# 
#     def __looking_at (self, word):
#         for i in range(len(word)):
#             t = self.offset + i
#             if t >= len(self.line): return False
#             if self.line[t] != word[i]: return False
#         return True
# 
#     def __scan_multi (self):
#         for word in self.syntax.multi:
#             if self.__looking_at(word):
#                 start = self.offset
#                 self.offset += len(word)
#                 self.__set_token(self.line[start:self.offset], start)
#                 return True
# 
#     ##  Whether the next token is something other than EOF.
#     #   If type or string is provided, the value indicates whether the next
#     #   token has the given type and/or string.
# 
#     def has_next (self, type=None, string=None):
#         if string:
#             if type: raise Exception("Provide only one argument")
#             return self.token() == string
#         elif type:
#             return self.token().hastype(type)
#         else:
#             return self.token().type != 'eof'
# 
#     ##  Iterator method.
# 
#     def __next__ (self):
#         token = self.token()
#         if token.type == 'eof': raise StopIteration
#         self.__token = None
#         self.old_linecount = self.linecount
#         self.old_offset = self.offset
#         return token
# 
#     ##  If the next token matches the given type and/or string, return it
#     #   and advance.  Otherwise, return None.
# 
#     def accept (self, type=None, string=None):
#         token = self.token()
#         if type and not token.hastype(type):
#             return None
#         if string and not (token == string):
#             return None
#         return next(self)
# 
#     ##  If the next token has the given type and/or string, return it
#     #   and advance.  Otherwise, signal an error.  Returns None at EOF.
# 
#     def require (self, type=None, string=None):
#         token = self.token()
#         if type and not token.hastype(type):
#             token.error('Expecting ' + repr(type))
#         if string and not (token == string):
#             token.error('Expecting ' + repr(string))
#         if type == 'eof': return None
#         else: return next(self)
# 
#     ##  Signal an error, indicating filename and line number.
# 
#     def error (self, msg=None):
#         token = self.token()
#         token.error(msg)
# 
#     ##  Print a warning, showing filename and line number.
# 
#     def warn (self, msg=None):
#         token = self.token()
#         token.warn(msg)
# 
#     ##  Push the current syntax on the stack and switch to the given syntax.
# 
#     def push_syntax (self, syntax):
#         self.stack.append(self.syntax)
#         self.syntax = syntax
#         self.__retreat()
# 
#     ##  Restore the previous syntax from the stack.
# 
#     def pop_syntax (self):
#         if not self.stack: raise Exception('Empty stack')
#         self.syntax = self.stack.pop()
#         self.__retreat()



#--  pprint  -------------------------------------------------------------------

##  A PPrinter instance.
pprint = None


##  Indentation for a PPrinter.

class PPrintIndent (object):

    ##  Constructor.

    def __init__ (self, pprinter, n):

        ##  The pprinter.
        self.pprinter = pprinter

        ##  The number of spaces indented by.
        self.n = n

    ##  Enter.

    def __enter__ (self):
        self.pprinter._indent += self.n

    ##  Exit.

    def __exit__ (self, t, v, tb):
        self.pprinter._indent -= self.n
        

##  A color for a PPrinter.

class PPrintColor (object):

    ##  Constructor.

    def __init__ (self, pprinter, color):

        ##  The pprinter.
        self.pprinter = pprinter

        ##  The color.
        self.color = color

        ##  Saves the previous color.
        self.prevcolor = None

    def _set_color (self, color):
        self.pprinter._color = color
        sys.stdout.write(fg[color])
        sys.stdout.flush()

    ##  Enter.

    def __enter__ (self):
        self.prevcolor = self.pprinter._color or 'default'
        self._set_color(self.color)

    ##  Exit.

    def __exit__ (self, t, v, tb):
        self._set_color(self.prevcolor)


##  A pretty-printer.

class PPrinter (object):

    ##  Constructor.

    def __init__ (self, file=None):
        self._color = None
        self._indent = 0
        self._atbol = True
        self._brflag = False
        self._file = file
    
    ##  String representation.

    def __repr__ (self):
        return '<PPrinter %s>' % repr(self._file)

    ##  The protected file.

    def file (self):
        if self._file is None: return sys.stdout
        else: return self._file

    ##  Returns an indentation.  Calling this in a with-statement causes the
    #   indentation to be active within the body.

    def indent (self, n=2):
        return PPrintIndent(self, n)

    ##  Start an indentation.  One should usually do "with pp.indent()" instead.

    def start_indent (self, n=2):
        self._indent += n
    
    ##  End an indentation.

    def end_indent (self, n=2):
        self._indent -= n
        if self._indent < 0: self._indent = 0
    
    ##  Freshline.

    def br (self):
        self._brflag = True

    ##  Returns a color.  Calling this in a with-statement causes the color
    #   to be used in the body.

    def color (self, c):
        return PPrintColor(self, c)

    ##  Like print().  Handles embedded newlines correctly.

    def __call__ (self, *args, end=None, color=None):
        if color is None:
            self._call1(args, end)
        else:
            with self.color(color):
                self._call1(args, end)
                
    def _call1 (self, args, end):
        if end is None and (len(args) == 0 or not hasattr(args[-1], '__pprint__')):
            end = '\n'
        first = True
        for arg in args:
            if first: first = False
            else: self.file().write(' ')
            self._printarg(arg)
        if end:
            self._printarg(end)

    def _printarg (self, arg):
        if hasattr(arg, '__pprint__'):
            arg.__pprint__()
        else:
            self.write(str(arg))

    ##  Write a string.

    def write (self, s):
        f = self.file()
        i = 0
        n = len(s)
        while i < n:
            j = s.find('\n', i)
            if j < 0: j = n
            # it is possible that s[0] == '\n'
            if i < j:
                if self._brflag and not self._atbol:
                    f.write('\n')
                    self._atbol = True
                if self._atbol:
                    f.write(' ' * self._indent)
                f.write(s[i:j].replace('\x1b', '\\x1b'))
                self._atbol = False
            # if j < n then s[j] == '\n'
            if j < n:
                f.write('\n')
                j += 1
                self._atbol = True
            i = j
    
    ##  Emit a newline, unless the last character printed was a newline.

    def freshline (self):
        if not self._atbol:
            self.write('\n')

    ##  Print and immediately flush.

    def now (self, *args, end=''):
        self.__call__(*args, end)
        self.file().flush()
    
    ##  Flush the output.

    def flush (self):
        self.file().flush()


pprint = PPrinter()


#--  redirect  -----------------------------------------------------------------
#
# with redirect() as f:
#     pprint('foo')
#     with pprint.indent():
#         pprint('bar')
#     return str(f)
#

class redirect (object):

    def __init__ (self, filename=None, mode='w', stderr=False):
        self.filename = filename
        self.mode = mode
        self._redirect_stderr = stderr
        self._file = None
        self._old_stdout = None
        self._old_stderr = None

    def __enter__ (self):
        if self.filename is None:
            self._file = StringIO()
        else:
            self._file = open(self.filename, self.mode)
        self._file.__enter__()
        self._old_stdout = sys.stdout
        sys.stdout = self._file
        if self._redirect_stderr:
            self._old_stderr = sys.stderr
            sys.stderr = self._file
        return self

    def __str__ (self):
        if self.filename is None and self._file is not None:
            return self._file.getvalue()
        else:
            return f'redirect({self.filename}, {self.mode})'
            
    def __exit__ (self, t, v, tb):
        sys.stdout = self._old_stdout
        if self._redirect_stderr:
            sys.stderr = self._old_stderr
        return self._file.__exit__(t, v, tb)
