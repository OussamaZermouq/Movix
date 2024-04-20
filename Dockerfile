FROM python:3.11

ADD bot.py .

RUN pip install requests beautifulsoup API_requests discord urllib dotenv

CMD ["python", "bot.py"]

