FROM python:3.11

ADD bot.py .
ADD * .
RUN pip install requests 
RUN pip install beautifulsoup4
RUN pip install discord 
RUN pip install urllib3
RUN pip install python-dotenv
RUN pip install wget

CMD ["python", "bot.py"]

