# 批量开放 iptables 端口
- [Linux中iptables防火墙指定端口范围](http://www.111cn.net/sys/linux/45525.htm)

```
-A INPUT -m state --state NEW -m tcp -p tcp --dport :8000 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 9000:-j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 8000:9000 -j ACCEPT
```
1. `8000:9000`  表示8000到9000之间的所有端口
2. `:8000`   表示8000及以下所有端口
3. `9000:`   表示9000以及以上所有端口


# mysql 日志记录
- [MySQL 错误日志(Error Log)](https://blog.csdn.net/leshami/article/details/39759849)

出问题了，只能周末时间充裕，再进行编译了。现在主要是写api。