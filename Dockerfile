FROM node:12
RUN apt-get update
RUN apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev nodejs
RUN curl -O https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz
RUN tar -xf Python-3.8.2.tar.xz
RUN cd /Python-3.8.2 && ./configure --enable-optimizations  && make -j `nproc` && make altinstall
RUN npm i -g vue-cli@2.9.6
ADD . /code
WORKDIR /code/vue
RUN npm install bootstrap-vue bootstrap webpack-dev-server
WORKDIR /code
RUN python3.8 -m pip install -r flask/requirements.txt
CMD ./run.sh