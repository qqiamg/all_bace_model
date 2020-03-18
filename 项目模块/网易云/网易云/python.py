import execjs
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def js_aes(text):
    jscode = """
    function encryptByAES(pwd) {
        var cryptoJS = require("crypto-js");

        let i = cryptoJS.enc.Utf8.parse("12345678901234561234567890123456");
        let t = cryptoJS.enc.Utf8.parse(pwd);
        let o = cryptoJS.enc.Utf8.parse("1234567890123456");
        return cryptoJS.AES.encrypt(t, i, {
                    iv: o,
                    mode: cryptoJS.mode.CBC,
                    padding: cryptoJS.pad.Pkcs7
                }).ciphertext.toString()
    }
    """
    ctx = execjs.compile(jscode)
    encrypto = ctx.call("encryptByAES", text)

    return encrypto


def py_aes(text):
    key = b"12345678901234561234567890123456"  # 长度必须为16
    text = text.encode("utf-8")

    cryptor = AES.new(key, AES.MODE_CBC, iv=b"1234567890123456")
    pad = 16 - len(text) % 16
    text = text + (chr(pad) * pad).encode("utf-8")  # 相当于JS里面的 padding: cryptoJS.pad.Pkcs7
    ciphertext = cryptor.encrypt(text)

    return b2a_hex(ciphertext).decode("utf-8")


text = "!abc123你好"
js_res = js_aes(text)
py_res = py_aes(text)

print(js_res == py_res)
print(js_res)
print(js_res)
