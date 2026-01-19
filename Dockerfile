FROM python:3.11.14-trixie

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

CMD ["python", "-m", "src.ui.test_ui"]