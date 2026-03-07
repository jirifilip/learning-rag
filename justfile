set shell := ["powershell.exe", "-c"]


monitoring-destroy:
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml down -v

monitoring:
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml down
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml up
