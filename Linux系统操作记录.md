麻蛋 看网上的PHP进阶资料，真是可笑啊，PHP的进阶就是去学其他的编程语言，C/C++, Linux     
也就是PHP的真正实力不在PHP自身，而在于对编程语言的深入了解也掌握。  

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

## 外键关联
- [大家设计数据库时使用外键吗？ ](https://www.zhihu.com/question/19600081) 外键使用利弊
- [MYSQL外键(Foreign Key)的使用](http://www.cppblog.com/wolf/articles/69089.html) 外键的语法讲解
- [MySQL的外键，自己的一点理解](https://www.programcat.com/index/info/id/2)     

= = 对数据库了解实在太少，如何优化性能，数据库高效率查询原理是什么，上百万的数据如何优化等等，我需要一本砖头书。    

外键的作用,主要有两个: 一个是让数据库自己通过外键来保证数据的完整性和一致性， 一个就是能够增加ER图的可读性。        
有些人认为外键的建立会给开发时操作数据库带来很大的麻烦，因为数据库有时候会由于没有通过外键的检测而使得开发人员删除，插入操作失败，他们觉得这样很麻烦， 其实这正式外键在强制你保证数据的完整性和一致性，这是好事儿。     

数据库服务器的性能不是问题，所以不用过多考虑性能的问题；另外，使用外键可以降低开发成本，借助数据库产品自身的触发器可以实现表与关联表之间的数据一致性和更新；最后一点，使用外键的方式，还可以做到开发人员和数据库设计人员的分工，可以为程序员承担更多的工作量；      

项目初始阶段，使用外键是必须的，而且是强烈推荐使用外键，数据库自带的约束，这样可以让你的业务架构迅速成型。等项目的数据量越做越大，用户数越来越多的时候，那个时候，已经可以充分证明你的业务架构是正确的，这个时候你要是有性能瓶颈上的问题，完全可以把外键去除，转移到应用层实现。        

**外键的使用条件：**
1. 两个表必须是InnoDB表，MyISAM表暂时不支持外键（据说以后的版本有可能支持，但至少目前不支持）；
2. 外键列必须建立了索引，MySQL 4.1.2以后的版本在建立外键时会自动创建索引，但如果在较早的版本则需要显示建立； 
3. 外键关系的两个表的列必须是数据类型相似，也就是可以相互转换类型的列，比如int和tinyint可以，而int和char则不可以；

**外键的好处**：可以使得两张表关联，保证数据的一致性和实现一些级联操作；    

**外键的语法**
```sql
[CONSTRAINT symbol] FOREIGN KEY [id] (index_col_name, ...)
    REFERENCES tbl_name (index_col_name, ...)
    [ON DELETE {RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT}]
    [ON UPDATE {RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT}]
```
该语法可以在 `CREATE TABLE` 和 `ALTER TABLE` 时使用，如果不指定CONSTRAINT symbol，MYSQL会自动生成一个名字。     `ON DELETE`、`ON UPDATE`表示事件触发限制，可设参数：    
- `RESTRICT`（限制外表中的外键改动）
- `CASCADE`（跟随外键改动）
- `SET NULL`（设空值）
- `SET DEFAULT`（设默认值）
- `NO ACTION`（无动作，默认的）

mysql里提到外键，那就是和主键相对的。主表是主键（唯一标识），从表可以设立外键（foreign key），建立一个和主表的一个联系（关系），从表的外键就是这两个数据表的连接所在。      
外键有三种关系：级联（cascade）、 制空（set null）、禁止（no action/restrict）。主表和从表都要是innodb引擎才行。        
```sql
create table zhubiao(  
    id int not null primary key auto_increment,  
    name char(20) default '主表数据'  
) engine=innodb charset=utf8;  
```

**级联关系(cascade)**: 从表的数据跟随主表的变化而变化，从表的数据随主表的改变而改变。删除和更改主表，从表受影响，而动从表，只要在（外键值）范围内主表不受影响，在范围外（外键范围），无法删改从表。
```sql
CREATE TABLE congbiao(  
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,  
    zid INT,  
    name VARCHAR( 20 ) ,  
    FOREIGN KEY ( zid ) REFERENCES zhubiao( id ) ON DELETE CASCADE ON UPDATE CASCADE  
) ENGINE = INNODB CHARSET = utf8;
```

**制空（set null）**: 以主表为主，从表外键关联后，再双方都有数据后，主表的那个外键对应的字段如果改变（删改）了，从表对应的那条数据的外键为null  
```sql
    create table congbiao(zid int,  
    name varchar(20) default '球星',  
    foreign key(zid) references zhubiao(id) on delete set null on update set null  
)engine=innodb charset=utf8;
```

**禁止模式（no action）**: 这个模式以从表为主，就是当两边都有数据后，主表里如果要删除或更改一条数据，如过从表里有对应的数据，则主表不允许更改或删除，要先删除从表里对应的数据，主表里的数据才可以动。   
```sql
create table congbiao(zid int,  
    name char(10),  
    foreign key(zid) references zhubiao(id) on delete no action on update no action
)engine=innodb charset=utf8;  
```

## MySQL 数据类型
- [MySQL数据类型--浮点数类型和定点数类型](https://blog.csdn.net/u011794238/article/details/50902405)
- [MySQL数字类型int与tinyint、float与decimal如何选择](http://seanlook.com/2016/04/29/mysql-numeric-int-float/)
整数  int, tinyint
浮点数  float, double   
时间类型 datetime, timestamp    

数据库的数据都指定类型，这样查询存储都会非常地高效，内存会被充分地利用。    
同样地，C语言中，类型都被准确指定，程序是高效而精确的。 
写着PHP的代码，没有类型指定很方便，但是很多时候指定类型能带来更高效的性能，我是非常乐见的。 
精准的类型，精准变量，让程序更严谨，我也是很乐见的。    