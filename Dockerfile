FROM python:3.12.2

WORKDIR /app/web_dev

COPY requirements.txt .  

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install cryptography

COPY . /app/

COPY model/ /app/model/

EXPOSE 5000   

CMD ["python", "/app/web_dev/app.py"]