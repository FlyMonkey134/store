# 项目介绍:

### 基本功能
- 首页展示
- 商品展示
- 分词查询
	- 分词主要是解决数据库模糊查询性能低下的解决方案
- 用户模块
	- 注册
		- 发送注册邮件
		- 注册验证
	- 登录
	- 注销
- 展示
- 购物车
- 订单模块
	- 主要涉及数据库的安全问题，提交数据库时怎么使用事务与事务回滚
- admin后台
	- 主要是使用django admin制作一个简单后台管理界面，同时怎么在django-admin使用第三方插件（富文本编辑器）
### 涉及的python组件
- Django==1.11.7
- django-haystack==2.6.1
	- Whoosh==2.7.4
	- jieba==0.39
		- haystatck的中文依赖（whoosh本身对于中文的分词做不得太好）
- django-redis==4.8.0
	- django的redis依赖
- django-tinymce==2.6.0
	- django-admin中的富文本编辑器
	- olefile==0.44
- MySQL-python==1.2.5
	- mysql 依赖
- Pillow==4.3.0
	- 图片处理
- django文件上传依赖
- PyMySQL==0.7.11
		- mysql依赖包
- pytz==2017.3
- redis==2.10.6
	- redis的依赖
	
### git下载
``` git -clone 
