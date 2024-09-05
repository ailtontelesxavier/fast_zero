sudo snap refresh node --channel=22
docker exec -it 6ff75289739c bash

# gera SECRET_KEY no terminal
python
import secrets
secrets.token_hex(256)

# fazer migrate
docker exec -it b8d4ddba3a4a sh -c "poetry run alembic upgrade head"

# subir somento o banco para teste
docker-compose up -d fastzero_database

sudo snap install node --classic --channel=20
npm install pm2 -g


# atualizar 
$ cd /var/www/frontend-portal
$ sudo git pull https://fomentoto:senha@gitlab.com/fomentoto/frontend-portal.git
$ sudo npm run build
$ sudo pm2 restart all

//pm2 start npm --name "frontend" -- start
pm2 kill && pm2 resurrect
# resetar nginx
$ sudo systemctl restart nginx

# se erro remover 
$rm -rf node_modules
$rm -f package-lock.json
$npm cache clean --force
$npm install


# com docker
sudo docker build -t frontend-portal .
sudo docker run -d -p 3000:3000 frontend-portal
sudo docker ps


sudo docker stop ID_DO_CONTAINER
sudo docker start ID_DO_CONTAINER
sudo docker restart ID_DO_CONTAINER
sudo docker logs ID_DO_CONTAINER

# criando systemd
sudo nano /etc/systemd/system/frontend-portal.service
--Em seguida, adicione o seguinte conteúdo ao arquivo:
[Unit]
Description=Frontend Portal Docker Container
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run -d -p 3000:3000 frontend-portal
ExecStop=/usr/bin/docker stop -t 2 frontend-portal
ExecStopPost=/usr/bin/docker rm -f frontend-portal
WorkingDirectory=/var/www/frontend-portal

[Install]
WantedBy=multi-user.target



---------------
--Recarregue os serviços do Systemd
$ sudo systemctl daemon-reload
--Inicie o serviço do contêiner
$ sudo systemctl start frontend-portal
--Verifique o status do serviço
$ sudo systemctl status frontend-portal
--verifique o status do serviço
$ sudo systemctl enable frontend-portal
--Habilitar inicialização automática:
$ sudo systemctl enable frontend-portal