FROM python:3.12 AS base

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt


FROM base AS development

COPY requirements-dev.txt requirements-dev.txt
RUN python -m pip install -r requirements-dev.txt
ENV PATH="/app/scripts:$PATH"

# Pocho approach directly from the terminal:
# export PATH=$PWD/scripts:$PATH

# FROM base AS production
# COPY . /app
# WORKDIR /app
# ENTRYPOINT ["/bin/bash"]
# CMD ["uvicorn", "--host", "0.0.0.0" , "--port", "8000", "wordle_api.main:app"]

# docker build -t wordle_api --target production .
# docker run -it --rm -p 8000:8000 wordle_api