TEXT_FILE_EXTENSIONS = ('txt', 'md', 'csv', 'json', 'xml', 'yaml', 'yml', 'py', 'html', 'js', 'css',
                        'ts', 'jsx', 'tsx', 'php', 'java', 'c', 'cpp', 'h', 'hpp', 'go', 'rb', 'rs',
                        'swift', 'kt', 'dart', 'lua', 'sh', 'bash', 'zsh', 'pl', 'perl', 'r', 'sql',)

IMAGE_FILE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'svg', 'ico')

PYTHON_KEYWORDS = ('def', 'class', 'import', 'from', 'as', 'if', 'else', 'elif', 'while', 'for', 
                   'break', 'continue', 'return', 'try', 'except', 'finally', 'with', 
                   'lambda', 'yield', 'raise', 'assert', 'del', 'global', 'nonlocal',
                   'pass', 'in', 'is', 'not')

C_KEYWORDS = ('auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
           'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
           'inline', 'int', 'long', 'register', 'return', 'short', 'signed',
           'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
           'unsigned', 'void', 'volatile', 'while')


def is_text_file(path):
    return path.split(".")[-1] in TEXT_FILE_EXTENSIONS
    
def is_image_file(path):
    return path.split(".")[-1] in IMAGE_FILE_EXTENSIONS

def is_pdf_file(path):
    return path.split(".")[-1] == 'pdf'

def is_python_file(path):
    return path.split(".")[-1] == 'py'

def is_python_keyword(word):
    return word in PYTHON_KEYWORDS

def is_c_file(path):
    return path.split(".")[-1] in ('c', 'cpp', 'h', 'hpp')

def is_c_keyword(word):
    return word in C_KEYWORDS
