FROM python:3.7-slim-buster AS builder

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git build-essential libatlas-base-dev

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --user -r requirements.txt && \
    pip install --user git+https://github.com/predsci/psidash.git
RUN pip install --user dash-extensions


FROM python:3.7-slim-buster AS runtime

COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

COPY . /home/audiolizer

WORKDIR /home/audiolizer/audiolizer

RUN jupyter serverextension enable jupytext

RUN pip install --upgrade dash

ENV AUDIOLIZER_TEMP /home/audiolizer/audiolizer/history

# # CMD jupyter notebook audiolizer/audiolizer.py --port=8888 --no-browser --ip=0.0.0.0 --allow-root

CMD python audiolizer.py


