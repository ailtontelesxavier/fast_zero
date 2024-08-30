FROM node:22-alpine3.19

WORKDIR /frontend

COPY package.json package-lock.json ./
#RUN npm install
# Execute o comando de construção do Next.js

COPY .env.local /frontend

COPY . .

RUN npm install -g npm@10.8.2 && npx next
RUN npm install glob@^9.0.0
#RUN npm install
RUN npm run build
RUN npm install pm2 -g


#CMD ["pm2-runtime", "start", "npm", "--", "start"]
#CMD ["pm2-runtime", "start", "npm", "--", "start", "--", "-H", "10.99.1.172"]
#CMD ["pm2-runtime", "start", "npm", "--", "start", "--", "-H", "nextjs"]
CMD ["pm2-runtime", "start", "npm", "--", "start"]

EXPOSE 3000
