
import codecs

unicode_escape_decoder = codecs.getdecoder('unicode-escape')

def parse_string(text):
    return unicode_escape_decoder(text[1:-1])[0]

def parse_num(text):
    return float(text) if '.' in text else int(text)