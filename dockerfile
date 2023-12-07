FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py loaddata fixtureDB.json

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]