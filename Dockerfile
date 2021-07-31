from python:3.8.5-alpine
workdir /app
add . /app
run pip3 install -r requirements.txt
CMD ["python3", "app.py"]
