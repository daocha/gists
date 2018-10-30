FROM python:3.6.6-alpine3.8

ENV FLASK_ENV="docker" \
	FLASK_APP="main.py"

COPY ./dcha /app/gists/dcha

COPY ./requirements.txt /app/gists/

EXPOSE 5000

RUN apk add --no-cache bash gcc build-base libffi-dev && \
		ln -s /app/gists/dcha/logs /app/logs

RUN pip3 install -r /app/gists/requirements.txt

WORKDIR /app/gists/dcha

CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]
