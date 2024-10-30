# Válasszunk egy alap Python képet
FROM python:3.9.20

# Szükséges csomagok telepítése
RUN pip install --no-cache-dir numpy
RUN pip install --no-cache-dir pandas
RUN pip install --no-cache-dir torch
RUN pip install --no-cache-dir torchvision
RUN pip install --no-cache-dir transformers
RUN pip install --no-cache-dir sentence-transformers

# A munkakönyvtár létrehozása a konténeren belül
WORKDIR /app

# Külső könyvtár felcsatolásához
VOLUME /app/config

# A Python programot GitHub-ról klónozzuk
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/robertlakatos/alchemy.git /app

# Parancs a Python program futtatásához
CMD ["python", "/app/main.py"]