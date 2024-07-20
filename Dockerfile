FROM python:3.11

ADD bot.py .

RUN pip install requests beautifulsoup discord urllib dotenv

CMD ["python", "bot.py"]

