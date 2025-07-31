#!/bin/bash

# Globale Umgebungsvariablen setzen
export REPO_OWNER="meinzeug"
export REPO_NAME="mrsunkwn"
export GITHUB_TOKEN="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"

# Anzahl der Instanzen
count=30

# Starte Agenten im Hintergrund
for ((i=1; i<=count; i++)); do
  echo "Starte Frontend Agent Nummer $i..."
  ./start_frontend_agent.sh &
  sleep 0.5  # Optional: Vermeidung gleichzeitiger Starts
done

echo "Alle $count Frontend Agents wurden gestartet."
