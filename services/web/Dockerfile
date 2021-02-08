# pull official base image
FROM maxenceroux/spotify-web:latest
# set work directory
WORKDIR /usr/src/app/

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apt-get -y install python3-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/