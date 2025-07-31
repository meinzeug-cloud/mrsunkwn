#!/bin/bash

# Anzahl der Wiederholungen
count=30

# Loop zum Ausführen von start_backend_agent.sh
for ((i=1; i<=count; i++)); do
  echo "Starte Backend Agent Nummer $i..."
  ./start_backend_agent.sh &
  sleep 0.5  # Optional: kleine Pause zwischen Starts
done

echo "Alle $count Backend Agents wurden gestartet."
