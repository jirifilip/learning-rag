set shell := ["powershell.exe", "-c"]


monitoring-destroy:
    docker compose down -v

monitoring:
    docker compose down
    docker compose up
