# description
```
python不支持rsa是私钥加密，golang编译成so文件，让python调用: 
python does not support rsa as a private key encryption, 
golang is compiled into a so file for python to call
```
# build
```shell
go build -ldflags "-s -w" -buildmode=c-shared -o ./rsa_so/bin/rsa_darwin_arm.so ./go/main.go
```
# quick start
1. install rsa-so packe
```
pip install rsa-so
```
2. encrypt data
```python
import base64
from rsa_so import sign

# Replace it with your own private key
private_key = """-----BEGIN RSA PRIVATE KEY-----
ABCD.....FGHI
-----END RSA PRIVATE KEY-----"""
data_bytes = private_key.encode('utf-8')
# Base64 encode
encrypted_data = base64.b64encode(data_bytes).decode('utf-8')
sign.encrypt_by_rsa_private_key('hello,word!!', encrypted_data)

```