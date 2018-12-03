# 开发记录
开发api过程中遇到的问题，flask web 开发这本书，我只是囫囵吞枣地抄完代码，其中用到的不少扩展，我都没有仔细地看。 
SQLAlchemy, Flask-Script, Flask-Migrate, Flask-Login, Flask-HTTPAuth    
这些扩展以及Flask本身，我都没有仔细地搞清楚，所以写这个项目的过程中，需要不断熟悉了解框架扩展的特性。   
Flask 的应用实例的创建使用了工厂模式，Flask-Script 让flask在命令行的操作非常便利，权限验证以及路由映射都使用到了装饰器模式，装饰器我实在了解的太少，本身就是很复杂。   
Flask的模块化分配给了Blueprint 实现了，创建模块专属后缀，然后全局注册。 

记录遇到的这些问题，记录从中学习到的知识，这个项目能够让我成长，懂得怎么慢慢学习掌握陌生的知识，不会不要怕，有别人的讲解，有别人的示例，我可以先抄代码，然后慢慢熟悉理解。  

# 相关资源和项目
- [httpbin](https://httpbin.org) 测试request请求
- [HTTP Request & Response Service, written in Python + Flask.](https://github.com/requests/httpbin)
- [guicorn 是什么 wsgi http 服务器](http://www.cnblogs.com/ifkite/p/5460328.html)
- [Token-Based Authentication With Flask](http://www.cnblogs.com/ifkite/p/5460328.html) 太复杂了    
- [Flask扩展系列(八)–用户会话管理](http://www.bjhee.com/flask-ext8.html) 使用 Flask-Login 扩展
- [Flask扩展系列(九)–HTTP认证](http://www.bjhee.com/flask-ext9.html) 使用 Flask-HTTPAuth 扩展
- [Flask扩展系列(六)–缓存](http://www.bjhee.com/flask-ext6.html) Flask-Cache 扩展
- [Flask扩展系列(三)–国际化I18N和本地化L10N](http://www.bjhee.com/flask-ext3.html) Flask-Babel扩展
- [Flask扩展系列–自定义扩展](http://www.bjhee.com/flask-ext.html) 
- [RESTful Authentication with Flask](https://blog.miguelgrinberg.com/post/restful-authentication-with-flask)


# API权限管理设计
- [flask 角色权限控制](https://www.jianshu.com/p/79d658e83157)
- [自建装饰器实现权限控制](https://liqiang.io/book/chapter006/) 也是用位操作实现的权限验证
- [Flask 用户权限划分](https://hui.lu/yong-hu-shu-ju-ku-biao-jie-gou-hua-fen/)
- [Flask Restful API权限管理设计与实现](https://www.jianshu.com/p/b78744bd463b)
- [Flask-用户角色及权限](https://www.cnblogs.com/liushaocong/p/7426811.html)
- [flask 角色验证中位操作求解？](https://www.zhihu.com/question/50986481)
- [flask 角色验证中位操作求解](https://segmentfault.com/q/1010000005094754/a-1020000005099826)

flask web开发的权限是直接用数字表示，添加权限直接加一个数，移除权限直接减一个数，判断是否有某个权限，怎么弄？

= = 位与操作，卧槽，好高端。。。。          

User 模型中添加的 can() 方法在请求和赋予角色这两种权限之间进行位与操作。如果角色中包含请求的所有权限位，则返回 True ，表示允许用户执行此项操作。    
```python
def can(self, permissions):
    return self.role is not None and \
           (self.role.permissions & permissions) == permissions

def is_administrator(self):
    return self.can(Permission.ADMINISTER)
```

位操作：程序中的所有数在计算机内存中都是以二进制的形式存储的。位运算说穿了，就是直接对整数在内存中的二进制位进行操作。而`与`操作呢，就是有对应的两个二进位均为1时，结果位才为1，否则为0。       

**权限与角色二进制表示**
```python
# 程序的权限
FOLLOW 　　　　　　　　关注用户 　　　　　　       0x01
COMMET 　　　　　　　　在他人文章中发表评论　　0x02
WRITE_ARTICLES 　　　　写文章　　　　　　　　　0x04
MODERATE_COMMENTS    管理他人发表的评论　　　0x08
ADMINISTER 　　　　　　　管理员权限　　　　　　　0x80
# 用户角色
匿名　　　　　　　　0x00　　　　　　未登录的用户，在程序中只有阅读权限
用户　　　　　　　　0x07　　　　　　具有发表文章，发表评论和关注其他用户的权限。这是新用户的默认角色
协管员　　　　　　　0x0f　　　　　　 增加审查不当评论的权限
管理员　　　　　　　0xff　　　　　　　具有所有权限,包括修改其他用户所属角色的权限
```
这种只适合8位吧，还是更多？如果权限很多的话，就不适用了，小型的、简单的系统没问题，不适合扩展。         


# 登录以及权限验证
登录本身就代表权限划分的一种，未登录和登录能看到的内容是不一样的，登录用户又根据身份，进行权限的进一步的细分。  
flask 只提供了框架的基础，请求、响应、上下文，其他的都交给开发者自己实现。      

flask web 开发一书里的登录认证是由 flask_login 的 login_user 实现的。   

用户会话管理和登录验证，那么对于HTTP请求上的认证，比如Restful API请求的认证要怎么做呢？因为Restful API不保存状态，无法依赖Cookie及Session来保存用户信息，自然也无法使用Flask-Login扩展来实现用户认证。  


# TODO
1. 创建数据表及相关模型，并且填充数据  
2. 登录测试 token 验证  
3. 权限管理 
4. 引入 flask-restplus 以及 swagger api 文档生成    
5. react navtive 开发
6. PC 端 react 应用开发 

# 数据表

超链接，音频，视频，文本，图片，文档附件   这几种是资源的媒体形式，根本不用单独建表。   
而是要把这种类型的资源进行管理，超链接，音频，视频，图片，文档附件 都是需要单独管理的

资源管理可以参照 google keep 的瀑布流 以及颜色  

用户表 user         
权限表 permission - 管理用户, 管理内容      
角色表 role  - 超级管理员 1 内容管理员 11 普通用户 12       
资源标签表 category PHP Python HTML5 前端 Linux         
专题收集表 网络爬虫， react native app开发，微信公众号开发  收集        
资源内容表 存放各种资源的信息 - 主表  存放整个网站的资源信息        
资源链接表 存放各种资源的url的表    
资源媒体类别表  超链接，音频，视频，文本，图片，文档附件 - 记录整个网站的资源链接       
开发计划表  网站的问题反馈，后期的规划发展，TODO等等             

以专题为主，资源标签作为识别辅助    
= =  我就想写个小小的网站，居然也要创建这么多数据表，真是疯了。     
所有创建的表统计: user, permission, role, category, resources, rank, links, media_type, project, project_resources      
```sql
数据库名 resource
# 用户表
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(64) NOT NULL UNIQUE,
    `nickname` VARCHAR(64) COMMENT '昵称',
    `location` VARCHAR(64) COMMENT '位置',
    `about_me` VARCHAR(64) COMMENT '个人简介',
    `member_since` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    `last_seen` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE  CURRENT_TIMESTAMP COMMENT '最后登录时间',
    `role_id` INT NOT NULL DEFAULT 12 COMMENT '角色id',
    `email` VARCHAR(64) NOT NULL UNIQUE,
    `password_hash` VARCHAR(128),
    `avatar_hash` VARCHAR(32) COMMENT '头像',
    `confirmed` TINYINT(1) DEFAULT 0,
    INDEX `index_username` (`username`),
    FOREIGN KEY (role_id) REFERENCES `role`(id) ON DELETE CASCADE ON UPDATE CASCADE,
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci;
# 权限表
CREATE TABLE IF NOT EXISTS `permission` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) COMMENT '权限名',
    `code` VARCHAR(64) NOT NULL UNIQUE COMMENT '权限英文名',
);
# 角色表
CREATE TABLE IF NOT EXISTS `role` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) COMMENT '角色名',
    `code` VARCHAR(64) NOT NULL UNIQUE COMMENT '角色英文名',
    `default` TINYINT(1) DEFAULT 0 COMMENT '用户默认角色',
);
# 标签表
CREATE TABLE IF NOT EXISTS `category` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL UNIQUE COMMENT '标签名',
);
# 内容表
CREATE TABLE IF NOT EXISTS `resources` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(64) NOT NULL COMMENT '资源名',
    `content_md` TEXT COMMENT '资源内容 markdown纯文本',
    `content_html` TEXT COMMENT '资源内容 html',
    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
    `pin` TINYINT(1) DEFAULT 0 COMMENT '置顶',
    `hot` TINYINT(1) DEFAULT 0 COMMENT '加精',
    `clicks` INT DEFAULT 0 COMMENT '点击量',
    `status` TINYINT(1) DEFAULT 1 ,
    `author_id` INT  COMMENT '用户id',
    `cid` INT  COMMENT '分类id',
    FOREIGN KEY (author_id) REFERENCES `user`(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (cid) REFERENCES `category`(id) ON DELETE SET NULL ON UPDATE CASCADE,
);
# 点赞表
CREATE TABLE IF NOT EXISTS `likes` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `like` TINYINT(1) DEFAULT 0 '点赞',
    `unlike` TINYINT(1) DEFAULT 0 COMMENT '踩',
    `author_id` INT COMMENT '点赞用户',
    `source_id` INT COMMENT '内容id',
    FOREIGN KEY (source_id) REFERENCES `sources`(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (author_id) REFERENCES `user`(id) ON DELETE SET NULL ON UPDATE CASCADE,
);
# 资源链接表
CREATE TABLE IF NOT EXISTS `links` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) COMMENT '资源名',
    `link` VARCHAR(1000) COMMENT '超链接',
    `tid` INT COMMENT '媒体类型',
    `md5` VARCHAR(32) '资源hash值',
    `add_time` DATETIME COMMENT '添加时间',
    FOREIGN KEY (tid) REFERENCES `media_type`(id) ON DELETE SET NULL ON UPDATE CASCADE,
);
# 资源媒体类别
CREATE TABLE IF NOT EXISTS `media_type` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) COMMENT '媒体类型名',
);
# 专题收集表
CREATE TABLE IF NOT EXISTS `project` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) COMMENT '专题名',
    `cover` VARCHAR(2083) COMMENT '专题封面',
    `slug` VARCHAR(100) COMMENT '专题url后缀',
    `add_time` DATETIME COMMENT '添加时间',
);
# 专题资源关联表
CREATE TABLE IF NOT EXISTS `project_resources`(
    `pid` INT COMMENT '专题id',
    `rid` INT COMMENT '资源id',
    FOREIGN KEY (rid) REFERENCES `resources`(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (pid) REFERENCES `project`(id) ON DELETE SET NULL ON UPDATE CASCADE,
);
```