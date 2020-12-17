# AMOS_plan
## Vue.js set up
```bash
sudo apt install nodejs npm
sudo npm i -g vue-cli@2.9.6
sudo npm i -g @vue/cli
npm install bootstrap-vue bootstrap

```  
Для запуска:
```bash
npm run dev
```

## Docker

```
sudo docker build -t planexe .
sudo docker run --network host --rm -it -p 8080:8080 planexe
```