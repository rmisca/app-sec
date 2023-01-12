FROM python:3.12.0a3-slim-buster

WORKDIR /sec_app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]

