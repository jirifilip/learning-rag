set shell := ["powershell.exe", "-c"]


monitoring-destroy:
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml down -v --remove-orphans

monitoring:
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml down --remove-orphans
    docker compose -f deployment/monitoring/monitoring.docker-compose.yaml up

processing-destroy:
    docker compose -f deployment/processing/processing.docker-compose.yaml down -v --remove-orphans

processing:
    docker compose -f deployment/processing/processing.docker-compose.yaml down --remove-orphans
    docker compose -f deployment/processing/processing.docker-compose.yaml up
