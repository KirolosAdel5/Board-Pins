FROM python:alpine
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000