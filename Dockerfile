FROM python:3.12.2

WORKDIR /app/web_dev

COPY requirements.txt .  

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install cryptography

COPY . /app/

EXPOSE 5000   

CMD ["python","app.py"]