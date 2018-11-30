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


# MySQL 相关函数等
## UTC 时间问题
- [MySQL的时区是否应该设置为UTC？](https://codeday.me/bug/20170619/28746.html)
- [MySQL時間類型Timestamp和Datetime 的深入理解](https://hk.saowen.com/a/aa9cda6e72382ccdb409ec841aaff51c4b1535d94c8b81464b5c543fa8b6bafa)
- [How do you set a default value for a MySQL Datetime column?](https://stackoverflow.com/questions/168736/how-do-you-set-a-default-value-for-a-mysql-datetime-column)

CURRENT_TIMESTAMP() 本地当前时间
UTC_TIMESTAMP() UTC时间

```sql
create table test(
    id int,
    expire_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8
```

datetime 类型的字段默认值 设为 current_timestamp 是在 5.6 之后的    


##  记录 emoji 的 utf8mb4 编码问题
- [mysql使用utf8mb4经验吐血总结](http://seanlook.com/2016/10/23/mysql-utf8mb4/)
**utf8mb4_unicode_ci 与 utf8mb4_general_ci 如何选择**   
字符除了需要存储，还需要排序或比较大小，涉及到与编码字符集对应的 排序字符集（collation）。ut8mb4对应的排序字符集常用的有 utf8mb4_unicode_ci、utf8mb4_general_ci.        
utf8mb4_unicode_ci 是基于标准的Unicode来排序和比较，能够在各种语言之间精确排序 utf8mb4_general_ci 没有实现Unicode排序规则，在遇到某些特殊语言或字符是，排序结果可能不是所期望的。 但是在绝大多数情况下，这种特殊字符的顺序一定要那么精确吗。比如Unicode把ß、Œ当成ss和OE来看；而general会把它们当成s、e，再如ÀÁÅåāă各自都与 A 相等。     
utf8mb4_general_ci 在比较和排序的时候更快 utf8mb4_unicode_ci 在特殊情况下，Unicode排序规则为了能够处理特殊字符的情况，实现了略微复杂的排序算法。 但是在绝大多数情况下，不会发生此类复杂比较。general理论上比Unicode可能快些，但相比现在的CPU来说，它远远不足以成为考虑性能的因素，索引涉及、SQL设计才是。 我个人推荐是 utf8mb4_unicode_ci，将来 8.0 里也极有可能使用变为默认的规则。        

## MySQL 的注释符
- [四种mysql注释实例](http://www.manongjc.com/article/921.html)

注释符一: `#`       
注释符二：`-- `     
注释符三: `/* */`       
注释符四：`/*! *`       