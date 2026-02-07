# 将 LMS Demo 部署到 VPS

**重要：不要把 VPS 的 root 密码写在代码或仓库里，也不要发给别人。**

## 一、在本地准备

1. 把整个 `lms_demo` 文件夹打包（可排除 `__pycache__`、`.pyc`）：
   - 或用 Git：在项目里 `git add` / `git push`，在 VPS 上 `git clone`。
   - 或打成 zip 用 scp 传到 VPS。

## 二、登录 VPS

在你自己电脑上打开终端，用 **你自己的** 密码登录（不要写在文档里）：

```bash
ssh -p 34093 root@38.147.172.156
```

输入 root 密码后即可进入 VPS。

## 三、在 VPS 上安装环境并运行

### 1. 安装 Python 3 和 pip（如未安装）

```bash
apt update
apt install -y python3 python3-pip python3-venv
```

### 2. 上传或克隆项目到 VPS

例如放到 `/opt/lms_demo`：

- **方式 A：本地上传**（在你自己电脑上执行，把 `lms_demo` 换成你本机路径）

```bash
scp -P 34093 -r /path/to/lms_demo root@38.147.172.156:/opt/
```

- **方式 B：VPS 上 git clone**（若你已把代码推到 Git）

```bash
mkdir -p /opt && cd /opt
git clone <你的仓库地址> lms_demo
cd lms_demo
```

### 3. 在 VPS 上创建虚拟环境并安装依赖

```bash
cd /opt/lms_demo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 用 Gunicorn 启动（对外可访问）

```bash
source /opt/lms_demo/venv/bin/activate
cd /opt/lms_demo
gunicorn -w 2 -b 0.0.0.0:5000 "app:app"
```

- `-w 2`：2 个进程。
- `-b 0.0.0.0:5000`：监听所有网卡，端口 5000。
- 浏览器访问：`http://38.147.172.156:5000`

若 VPS 防火墙/安全组未放行 5000，需要开放：

```bash
# 若用 ufw
ufw allow 5000/tcp
ufw reload
```

（云厂商控制台里的“安全组”也要放行 5000。）

## 四、后台常驻运行（可选）

用 `nohup` 或 `systemd` 让服务一直跑。

### 方式 A：nohup

```bash
cd /opt/lms_demo
source venv/bin/activate
nohup gunicorn -w 2 -b 0.0.0.0:5000 "app:app" > gunicorn.log 2>&1 &
```

### 方式 B：systemd（推荐）

新建服务文件：

```bash
nano /etc/systemd/system/lms-demo.service
```

写入（路径按你实际部署的改）：

```ini
[Unit]
Description=LMS Demo Flask App
After=network.target

[Service]
User=root
WorkingDirectory=/opt/lms_demo
Environment="PATH=/opt/lms_demo/venv/bin"
ExecStart=/opt/lms_demo/venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 "app:app"
Restart=always

[Install]
WantedBy=multi-user.target
```

然后：

```bash
systemctl daemon-reload
systemctl enable lms-demo
systemctl start lms-demo
systemctl status lms-demo
```

## 五、用 Nginx 反代并可选绑定域名（可选）

若想用 80 端口或域名访问，可装 Nginx：

```bash
apt install -y nginx
```

新建站点配置，例如：

```bash
nano /etc/nginx/sites-available/lms-demo
```

内容示例（用 IP 访问时把 `server_name` 改成你的 IP 或域名）：

```nginx
server {
    listen 80;
    server_name 38.147.172.156;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用并重载：

```bash
ln -s /etc/nginx/sites-available/lms-demo /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

之后可用 `http://38.147.172.156` 访问（无需写 :5000）。

## 六、安全提醒

- **不要**在 DEPLOY.md、代码或仓库里写 root 密码或面板密码。
- 部署后建议：改 root 密码、配置 SSH 密钥登录、关闭密码登录（在确认密钥可用后）。
- 若对外网开放，可考虑只允许 Nginx 反代，Gunicorn 只监听 127.0.0.1。

## 七、常用命令速查

| 操作           | 命令 |
|----------------|------|
| 查看 Gunicorn 进程 | `ps aux \| grep gunicorn` |
| 停止 nohup 启动的 | `pkill -f "gunicorn.*app:app"` |
| 若用 systemd     | `systemctl restart lms-demo` |
| 看日志（systemd） | `journalctl -u lms-demo -f` |
