FROM bigsoulja/ord-regtest:latest

ENV HOME=/root
WORKDIR /app

COPY rune-farming.py /app/rune-farming.py
COPY create_batch_svg.py /app/create_batch_svg.py
COPY data /app/data