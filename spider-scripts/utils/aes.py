from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

class AESCipher:

    def decode_ecb_pkcs7(self, str_data, key):
        """
        AES解密函数
        """
        if not str_data or not key:
            return None
        
        # 将密钥转换为bytes
        key = key.encode('utf-8')
        
        # 将输入的字符串进行base64解码
        encrypted_data = base64.b64decode(str_data)
        
        # 创建AES解密器（ECB模式）
        cipher = AES.new(key, AES.MODE_ECB)
        
        # 解密数据
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # 去除PKCS7填充
        unpadded_data = unpad(decrypted_data, AES.block_size)
        
        # 将解密后的数据转换为字符串
        return unpadded_data.decode('utf-8')