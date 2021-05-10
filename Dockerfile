FROM python:3.7-alpine
ENV APP_PORT 8080
COPY . /app
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
EXPOSE 8080

CMD ["python", "currency_converter_api.py"]