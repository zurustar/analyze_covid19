FROM python:3.7.5-slim

RUN pip3 install --upgrade pip
RUN pip3 install pandas matplotlib

CMD ["python3", "/src/analyze.py", "/src", "result.csv", "result.png"]

