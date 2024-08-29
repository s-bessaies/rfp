FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh
# Install SQLite from source
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3430100.tar.gz && \
    tar xzf sqlite-autoconf-3430100.tar.gz && \
    cd sqlite-autoconf-3430100 && \
    ./configure && \
    make && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf sqlite-autoconf-3430100 sqlite-autoconf-3430100.tar.gz

COPY requirements.txt /app/
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc


COPY . /app/
# Specify the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
