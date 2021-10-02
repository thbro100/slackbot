FROM python:3.9.7-bullseye

WORKDIR /app

COPY requirments.txt .
RUN pip install -r requirments.txt

COPY /app .

CMD ["python","index.py"]