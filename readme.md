### 功能实现
通过协程方式并发扫描多台服务器的jar包,并将匹配的jar写入文件中


### 使用方法
参数二： 扫描的目录
参数三： 将结果写入的文件名
server_mana(server_list,"/data/scan_dir/test","jar_bugfile").compare()

### 启动方式
> 命令行
    
    sh restart.sh

> supervisor

    supervisorctl update 
    
# 使用过程中有任何问题，请加QQ：948190444
