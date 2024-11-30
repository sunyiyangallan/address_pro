import hashlib


def md5_encrypt(text):
    # 创建一个md5对象
    md5 = hashlib.md5()

    # 对字符串进行编码，然后更新md5对象
    md5.update(text.encode('utf-8'))

    # 获取加密后的十六进制字符串
    encrypted_text = md5.hexdigest()

    return encrypted_text