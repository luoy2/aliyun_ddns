# aliyun_ddns
update ddns ip to aliyun domain

folked from https://github.com/terencechuen/terence_proj/tree/master/aliyun_ddns

detail description: 
https://enginx.cn/2016/08/22/通过python将阿里云dns解析作为ddns使用.html

wrapped into class, and support python3.


## Requirement
##### python env:

| python version        | availability |
| ------------- |:-------------:|
|python 3.6| available |
|< python 3.5 | available     |
|python 2.x| unavailable |



# how to use:
0. `pip3 install -r requirements.txt`
1. request access key and access secret from aliyun(https://ak-console.aliyun.com/?spm=a3c0i.o25698zh.a3.2.7f43cc3anqW2D#/):
2. put the access key, secret, domain into a json file like `sample_key.json`
3. change global vairable `KEY_FILE_NAME` as your key file name
4. run main in a task scheduler
