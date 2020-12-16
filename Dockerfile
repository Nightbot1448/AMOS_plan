FROM ubuntu:20.04
ENV TZ=Europe/Moscows
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fsn /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install -y python3-dev python3-pip nodejs npm
RUN npm i -g vue-cli@2.9.6
ADD . /code
WORKDIR /code/vue
RUN npm install bootstrap-vue bootstrap webpack-dev-server
WORKDIR /code
RUN python3 -m pip install -r flask/requirements.txt
CMD ./run.sh