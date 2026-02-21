# Настраиваем деплой

```shell
sudo apt update && sudo apt upgrade -y
```

```shell
sudo apt install -y curl git nginx nano systemd
```


https://docs.astral.sh/uv/

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Активируем по инструкции из результата выполнения или просто перезаходим

```shell
bash
```

```shell
uv --version
```

Клонируем проект

```shell
cd /var
git clone https://github.com/mahenzon/micro-example-fastapi-app.git
```

```shell
cd micro-example-fastapi-app
```

Инициализируем venv и качаем питон. Можно просто через uv, там есть готовые сборки
```shell
uv venv --managed-python
```

Устанавливаем зависимости

```shell
uv sync --no-dev
```

Проверим, что оно стартует:

```shell
# активируем venv
source .venv/bin/activate

# стартуем app
fastapi dev

# можно в отдельном терминале попробовать дернуть
curl localhost:8000/items/
```


## systemd

Запускаем сервис в systemd

```shell
nano /etc/systemd/system/fastapi_app.service
```


Описываем конфиг

```ini
[Unit]
Description=FastAPI Application
After=network.target

[Service]
# your user
User=root
# your group
Group=root

# Your project directory
WorkingDirectory=/var/micro-example-fastapi-app

# Using the binary inside .venv directly
ExecStart=/var/micro-example-fastapi-app/.venv/bin/fastapi run app.py --host 127.0.0.1 --port 8000 --workers 2 --proxy-headers

# Environment configs
Environment="PYTHONUNBUFFERED=1"

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```shell
# 1. Reload the systemd daemon to read the new file
sudo systemctl daemon-reload

# 2. Start the service
sudo systemctl start fastapi_app

# 3. Enable it to run on boot
sudo systemctl enable fastapi_app

# 4. Check status (to see logs and ensure it started)
sudo systemctl status fastapi_app

# 5. Check logs
sudo journalctl -u fastapi_app -f
```

## nginx

Прокидываем статику к nginx, чтобы он это отдавал

```shell
ln -s /var/micro-example-fastapi-app/static /usr/share/nginx/micro_fastapi_app_static
```

Настраиваем доступ к файлам

```shell
# даем доступ через папку
chmod 711 /var/micro-example-fastapi-app
# даем доступ на чтение статики
chmod 755 /var/micro-example-fastapi-app/static
# а питон файлы доступны только владельцу
chmod 600 /var/micro-example-fastapi-app/*.py
```



```shell
sudo nano /etc/nginx/sites-available/micro_fastapi_app.conf
```

```nginx
upstream fastapi_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name localhost; # Replace with your IP or Domain (e.g., example.com)

    # --- STATIC FILES ---
    location /static {
        # Using the symlink location we established previously
        alias /usr/share/nginx/micro_fastapi_app_static;

        # Cache settings
        location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 30d;
            add_header Cache-Control "public, no-transform";
            access_log off;
        }
    }

    # --- MAIN APP PROXY ---
    location / {
        proxy_pass http://fastapi_backend;
        
        # Performance/WebSocket headers
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;

        # Identity headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```


```shell
ln -s /etc/nginx/sites-available/micro_fastapi_app.conf /etc/nginx/sites-enabled/
```

Проверяем конфигурацию. Должно быть всё ОК

```shell
nginx -t
```


Перезапускаем 

```shell
sudo service nginx restart
```


Дергаем локально

```shell
# можем проверить доступ к статике
curl localhost/static/js/swagger-ui-bundle.js 
# и к приложению
curl localhost/items/
```

Заходим извне по внешнему адресу (пока по HTTP).


## SSL

Устанавливаем certbot, если ещё нет

```shell
sudo snap install --classic certbot
```

И докидываем SSL сертификаты. 

```shell
sudo certbot --nginx
```

