import base64

def obfuscate_str(ori_str, key):
    enc = []
    for i in range(len(ori_str)):
        key_c = key[i % len(key)]
        enc_c = (ord(ori_str[i]) + ord(key_c)) % 256
        enc.append(enc_c)
    return (base64.urlsafe_b64encode(bytes(enc))).decode("utf-8")

def deobfuscate_str(enc_str, key):
    dec = []
    enc_str = base64.urlsafe_b64decode(enc_str)
    for i in range(len(enc_str)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + enc_str[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

print(obfuscate_str('user_id_1', 'somekey'))