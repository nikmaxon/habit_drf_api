FROM python:3

WORKDIR /homework_27_1

COPY ./requirements.txt /homework_27_1/

RUN python.exe -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]