FROM rasa/rasa
ENV BOT_ENV=production
COPY . /var/www
WORKDIR /var/www


ENTRYPOINT [ "rasa", "run", "-vv", "-m", "models/english_model.tar.gz", "-p", "8080", "--enable-api", "--cors", "*"]