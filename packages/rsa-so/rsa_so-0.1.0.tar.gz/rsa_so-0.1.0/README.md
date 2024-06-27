# description
```azure
python不支持rsa是私钥加密，golang编译成so文件，让python调用: 
python does not support rsa as a private key encryption, 
golang is compiled into a so file for python to call
```
# build
```
go build -ldflags "-s -w" -buildmode=c-shared -o ./rsa_so/bin/rsa_darwin_arm.so ./go/main.go
```