1. nak activate venv
.venv\Scripts\activate

2. install grpc inside venv
pip install grpcio grpcio-tools


STEP TO RUN :
1. Tutup semua running docker
docker compose down -v

2. run balik semua
docker compose up --build

3. untuk test client, open a new terminal then masuk balik venv environment, then run client
python client_test.py (untuk grpc in docker sahaja)
python client_rest_test.py (untuk rest in docker sahaja)

EXTRA NOTES:
In Dockerfile for each service, please comment the cmd that you dont want use.
For example if want to run grpc the comment on cmd for rest_server.py

4. To end docker session
ctrl + c


#Kalau ada edit docker file:
docker compose down

# Langkah 2a: Paksa bina semula semua imej tanpa cache
docker compose build --no-cache 

# Langkah 2b: Mulakan stack
docker compose up -d