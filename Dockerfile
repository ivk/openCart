# base image
FROM python:3.10-alpine

# workdir inside the image
WORKDIR /app

# requirements file must exists
COPY requirements.txt .

# install requirements
RUN pip install -U pip && pip install -r requirements.txt

COPY tests/test*.py  tests/
COPY conftest.py .

#CMD ["pytest"]

ENTRYPOINT ["pytest"] 
