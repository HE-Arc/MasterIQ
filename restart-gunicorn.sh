# Auteur: Stéphane Oguey

# Trouver les ID des processus Gunicorn
PIDS=$(pgrep gunicorn)

# Si des processus Gunicorn sont en cours d'ex  cution
if [ -n "$PIDS" ]; then
    # Tuer les processus Gunicorn
    kill -9 $PIDS
fi

sudo systemctl restart gunicorn

echo "Gunicorn restart done."