# Fastapi Crawl Admin
[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/Python-3.8.0-green&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/Celery-5.0.5-blue&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/Fastapi-0.4.9-red&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/uvicorn-0.2.2-yellow&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/pydantic-0.2.2-brightgreen&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/fabric-0.1.13-yellow&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/vue-2.6.10-brightgreen&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/element--ui-2.8.2-brightgreen&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/releases-0.1.0-yellow&#41;)

[comment]: <> (![Fastapi Crawl]&#40;https://img.shields.io/badge/license-MIT-red&#41;)

> 基于 `Fastapi` + `Vue` + `Element UI` 的 `分布式爬虫系统`。

- [线上地址]()
- [中文文档]()

## 后端 API
![Fastapi Crawl](https://img.shields.io/badge/Python-3.8.0-green)
![Fastapi Crawl](https://img.shields.io/badge/Celery-5.0.5-blue)
![Fastapi Crawl](https://img.shields.io/badge/Fastapi-0.4.9-red)
![Fastapi Crawl](https://img.shields.io/badge/uvicorn-0.2.2-yellow)
![Fastapi Crawl](https://img.shields.io/badge/pydantic-0.2.2-brightgreen)
![Fastapi Crawl](https://img.shields.io/badge/fabric-0.1.13-yellow)
## alembic 生成表

### 自动生成迁移文件

```shell
alembic revision --autogenerate -m "init commit"
```

### 生成表
```shell
alembic upgrade head
```

### 生成初始化账号密码

```shell
cd app
python initial_data.py
```

```shell
username: admin@163.com
password: 123456
```

## 前端项目

![Fastapi Crawl](https://img.shields.io/badge/vue-2.6.10-brightgreen)
![Fastapi Crawl](https://img.shields.io/badge/element--ui-2.8.2-brightgreen)
![Fastapi Crawl](https://img.shields.io/badge/license-MIT-red)
![Fastapi Crawl](https://img.shields.io/badge/releases-0.1.0-yellow)


前端项目基于 [vue-manage-system](https://github.com/lin-xin/vue-manage-system) 模板构建
, 
 感谢作者。

### 项目截图

![Image text](https://github.com/lin-xin/manage-system/raw/master/screenshots/wms3.png)


### 功能

-   [x] 登录/注销
-   [x] Dashboard
-   [x] 支持切换主题色 :sparkles:
-   [x] 远程批量部署和调用
-   [x] 任务日志
-   [x] 新增节点、测试节点
-   [x] 主机节点详细指标
-   [x] 国际化
-   [ ] 权限管理
-   [ ] 站内消息推送


### 安装步骤

```
 // 把模板下载到本地
git clone https://github.com/PY-GZKY/fastapi-crawl-admin.git     

// 进入模板目录
cd crawlfont    

// 安装项目依赖，等待安装完成之后，安装失败可用 cnpm 或 yarn
npm install         

// 开启服务器，浏览器访问 http://localhost:8080
npm run dev

// 执行构建命令，生成的dist文件夹放在服务器下即可访问
npm run build
```


### 二、如何切换主题色呢？

第一步：打开 `src/main.js` 文件，找到引入 element 样式的地方，换成浅绿色主题。

```javascript
import 'element-ui/lib/theme-default/index.css'; // 默认主题
// import './assets/css/theme-green/index.css';       // 浅绿色主题
```

第二步：打开 src/App.vue 文件，找到 style 标签引入样式的地方，切换成浅绿色主题。

```javascript
@import "./assets/css/main.css";
@import "./assets/css/color-dark.css";     /*深色主题*/
/*@import "./assets/css/theme-green/color-green.css";   !*浅绿色主题*!*/
```


## License
[MIT](https://github.com/PY-GZKY/fastapi-crawl-admin/LICENSE)
