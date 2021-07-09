# Signal to the distributor cron job that we want a license
touch /tmp/waiting.flag

while [ ! -f /usr/local/stata17/stata.lic ]; do sleep 1; echo "Waiting for license."; done
echo "Spawning Stata session."

stata &
rm /usr/local/stata17/stata.lic

# Entrypoint to jupyter notebook
start.sh
