FROM python:3.11


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV S6_VERSION=v2.1.0.2
ENV SHINY_SERVER_VERSION=latest
ENV PANDOC_VERSION=default

RUN /app/install_shiny_server.sh

EXPOSE 8000

RUN rm -rf /etc/shiny-server/shiny-server.conf \
    && cp /app/shiny-server.conf /etc/shiny-server/ \
	&& rm -rf /srv/shiny-server/* \
	&& cp -r /app/. /srv/shiny-server/ 

ENTRYPOINT ["/init"]



#ENTRYPOINT ["shiny", "run" , "app.py"]
