# seeding 富途牛牛种子脚本
> 支持以下功能
>  - 种子浇水
>  - 好友浇水
## 使用教程
> 安装python3
```bash
apt install python3.10
```
> 安装依赖
```bash
pip3 install -r requirements
```
> 设置 uid 和 web_sig
```bash
https://seed.futunn.com/
cookie 获取 uid 和 web_sig
```
> 设置crontab脚本
```bash
0 */2 * * * python3 path/main.py
```