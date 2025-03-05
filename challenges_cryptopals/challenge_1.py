import binascii
import base64

def hex_to_base64(_hexString):
    rawBytes = binascii.unhexlify(_hexString)
    
    return base64.b64encode(rawBytes).decode()

string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
print(hex_to_base64(string))