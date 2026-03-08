set shell := ["powershell.exe", "-c"]


monitoring-destroy:
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml down -v

monitoring:
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml down
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml up

processing-destroy:
    docker compose -f deployment/processing/processing.docker-compose.yaml down -v

processing:
    docker compose -f deployment/processing/processing.docker-compose.yaml down
    docker compose -f deployment/processing/processing.docker-compose.yaml up
