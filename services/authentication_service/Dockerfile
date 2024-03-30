FROM python:alpine
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
COPY certificate.crt /usr/src/app
COPY private.key /usr/src/app

CMD ["python", "manage.py", "runsslserver", "0.0.0.0:8000", "--certificate", "/usr/src/app/certificate.crt", "--key", "/usr/src/app/private.key"]

EXPOSE 8000