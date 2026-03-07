set shell := ["powershell.exe", "-c"]

monitoring:
    docker compose down
    docker compose up
