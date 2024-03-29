FROM python:3.8-slim-buster
# gcc g++ libqpdf-dev
RUN apt-get update && apt-get install -y sane-utils libsane-hpaio imagemagick tesseract-ocr-fra tesseract-ocr-deu ocrmypdf nano
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml
CMD ["python", "./main.py"]