FROM python:3-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . /app
RUN pip install PEP517
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]