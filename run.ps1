# Script pour lancer AskIT-CLI sans création de __pycache__
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "Lancement d'AskIT-CLI (sans __pycache__)..." -ForegroundColor Green
poetry run askit-cli $args 