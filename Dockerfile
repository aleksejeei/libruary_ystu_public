FROM python:latest
WORKDIR /app
COPY db /app/db
COPY filters /app/filters
COPY handlers /app/handlers
COPY parser /app/parser
COPY accepts.py /app/accepts.py
COPY keyboards.py /app/keyboards.py
COPY main.py /app/main.py
COPY push.py /app/push.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]