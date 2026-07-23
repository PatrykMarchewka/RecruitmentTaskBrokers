FROM python:3.14

# Create nonroot user for security
RUN useradd -m appuser

WORKDIR /app
USER appuser

# Required dependencies
RUN pip install --no-cache-dir \
    asgiref==3.12.1 \
    Django==6.0.7 \
    djangorestframework==3.17.1 \
    sqlparse==0.5.5 \
    typing_extensions==4.16.0 \
    tzdata==2026.3

# Fix potential permission issues
COPY --chown=appuser:appuser main .

# 0.0.0.0 to listen on every IP, used inside Docker so it cant be mapped to 127.0.0.1 on localhost
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]