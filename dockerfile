FROM python:3.12

WORKDIR /hungaro/

#Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /hungaro/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . /hungaro/

ENV PYTHONPATH=/hungaro
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "metodo_hungaro_api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]