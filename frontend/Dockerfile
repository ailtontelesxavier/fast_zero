# Use a imagem base do Node.js com Alpine Linux
FROM node:22-alpine3.19

# Defina o diretório de trabalho
WORKDIR /app

# Copie apenas os arquivos de dependências para a imagem
COPY package.json package-lock.json ./

# Instale o tzdata para configurar o fuso horário usando apk
RUN apk add --no-cache tzdata && \
    ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

# Defina a variável de ambiente TZ para o fuso horário correto
ENV TZ="America/Sao_Paulo"

# Instale as dependências do projeto
RUN npm install

# Copie as variáveis de ambiente
COPY .env.local .env.production ./

# Copie o restante do código do projeto
COPY . .

# Instale a versão específica do npm globalmente
RUN npm install -g npm@10.8.2

# Instale dependências adicionais
#RUN npm install -g glob@^10.4.5

# Construa o projeto Next.js
RUN npm run build

# Instale o PM2 globalmente para gerenciar processos
RUN npm install pm2 -g

# Defina o comando de inicialização usando PM2 para gerenciar o processo de produção
CMD ["pm2-runtime", "npm", "--", "start"]

# Exponha a porta que o aplicativo Next.js usará
EXPOSE 3000
