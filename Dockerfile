#Docker File for build CS50 Project 4 Networks Assignment by N. Sekar
FROM python:3
COPY .  /usr/src/app
WORKDIR /usr/src/app
EXPOSE 8080
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "8080"]
