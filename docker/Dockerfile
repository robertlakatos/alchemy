# Válasszunk egy alap Python képet
FROM python:3.9.20

# Szükséges csomagok telepítése
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir numpy
# RUN pip install --no-cache-dir pandas
# RUN pip install --no-cache-dir torch
# RUN pip install --no-cache-dir torchvision
# RUN pip install --no-cache-dir transformers
# RUN pip install --no-cache-dir sentence-transformers
# RUN pip install  --no-cache-dir -U "huggingface_hub[cli]"

# Külső könyvtár felcsatolásához
VOLUME /alchemy/codes/mount

# A Python programot GitHub-ról klónozzuk
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/robertlakatos/alchemy.git

# Huggingface token beállítása
RUN huggingface-cli login --token hf_**** --add-to-git-credential

# Log könyvtár létrehozása
RUN mkdir -p /alchemy/logs

# Kimenet bufferelés letiltása, hogy a log fájlban azonnal megjelenjen az info.
ENV PYTHONUNBUFFERED=1

# A munkakönyvtár létrehozása a konténeren belül
WORKDIR /alchemy/codes

# Parancs a Python program futtatásához
CMD ["tail", "-f", "/dev/null"]
# CMD ["sh", "-c", "python server.py >> /alchemy/logs/alchemy.log 2>&1"]

# Port kiadása
EXPOSE 20249