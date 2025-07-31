#!/bin/bash

# Anzahl der Wiederholungen
count=30

# Loop zum Ausführen von start_backend_agent.sh
for ((i=1; i<=count; i++)); do
  echo "Starte Frontend Agent Nummer $i..."
  ./start_frontend_agent.sh &
  sleep 0.5  # Optional: kleine Pause zwischen Starts
done

echo "Alle $count Frontend Agents wurden gestartet."
