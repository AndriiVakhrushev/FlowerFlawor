FROM python:3.6

RUN mkdir -p /usr/src/bloomon/
WORKDIR /usr/src/bloomon/
COPY . /usr/src/bloomon/

RUN pip install --no-cache-dir -r requirements.txt



CMD ["python", "manage.py"]