#!/bin/bash

# Globale Umgebungsvariablen setzen
export REPO_OWNER="meinzeug"
export REPO_NAME="mrsunkwn"
export GITHUB_TOKEN="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"

# Anzahl der Instanzen
count=1000

# Starte Agenten im Hintergrund
for ((i=1; i<=count; i++)); do
  echo "Starte Backend Agent Nummer $i..."
  ./start_backend_agent.sh &
  sleep 0.5  # Optional: Vermeidung gleichzeitiger Starts
done

echo "Alle $count Backend Agents wurden gestartet."
