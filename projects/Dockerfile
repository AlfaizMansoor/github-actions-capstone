 # This is a test Docker file to Dockerize a full Application
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd \
	&& rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt
RUN useradd -m bankemployee 
COPY . .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh && chown -R bankemployee /app
USER bankemployee
EXPOSE 5000
CMD ["sh", "entrypoint.sh"]
