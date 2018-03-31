#!/usr/bin/env python
#coding:utf-8
#2018.3.28 wangsiyuan




#. jar包md5扫描：
#    1. 列出严重bug的jar包
#    2. 全局扫描jar包，列出md5
#4. 比较md5.弄个脚本，全局扫描
#并发连接到所有服务器中





from gevent import monkey; monkey.patch_all()
import gevent,time,os
from app.sshconn import SSHConnection


class server_mana(object):
    def __init__(self,server_list,path,bugfile):
        self.server_list = server_list
        self.path = path
        self.bugfile = bugfile
        self.list = []
        self.dict = {}

    def server_split(self,server):
        return server.split(":")


    def coroutine(self):
        """实现协程"""
        gevent.joinall(
            [gevent.spawn(self.shell,i) for i in self.server_list]
        )


    def _dict(self):
        try:
            self.list = list(set(self.list)) #去重
            print self.list
            for i in self.list:
                a = i.split()
                if len(a) == 2:
                    self.dict[a[0]] = a[1]
        except:
            print "_dict 分割字符串出错了"


    #判断 服务器中是否有 bug 的 jar
    def compare(self):
        while True:
            self.coroutine()
            self._dict()
            with open(self.bugfile,"w") as f:
                for i in jar_md5_list:
                    if self.dict.has_key(i):
                        #有的话在这里执行,需要的操作
                        f.write(self.dict[i])

            time.sleep(5)



    def shell(self,server):
        serList = self.server_split(server)
        conn = SSHConnection(serList[0], int(serList[1]), serList[2], serList[3])
        cmd = "find %s -name \"*.jar\" | xargs md5sum" %self.path
        result = conn.exec_command(cmd)
        self.list = self.list + result.split("\n")
        conn.close()


if __name__ == '__main__':
    # 有 bug jar包 MD5值,需要修改有 bug的 jar md5值
    jar_md5_list = [
        "f69728e49bf94c32306c36875d5ff00e",
        "f69728e49bf94c32306c36875d5ff001",
        "9c45ac1aa8ea102f6cd964f35454048f"
    ]


    #服务器IP:端口:用户:密码
    server_list = [
        "192.168.222.140:22:root:123456",
        "192.168.222.140:22:root:123456",
        "192.168.222.140:22:root:123456",
        "192.168.222.140:22:root:123456",
        "192.168.222.140:22:root:123456",

    ]

    # 创建进程pid file
    with open("/run/scan_dir.pid", "w") as f:
        f.write(str(os.getpid()))


    server_mana(server_list,"/data/scan_dir/test","jar_bugfile").compare()
