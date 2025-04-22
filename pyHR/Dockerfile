
FROM python:3.13

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY .env /code
COPY alembic.ini /code
COPY /migrations /code


CMD ["alembic", "upgrade", "head"]
CMD ["fastapi", "run", "app/main.py", "--port", "80"]