# pull official base image
FROM maxenceroux/spotify-web
# set work directory
WORKDIR /usr/src/app/

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/