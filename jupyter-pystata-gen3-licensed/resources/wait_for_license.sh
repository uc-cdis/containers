# Signal to the distributor cron job that we want a license
touch /tmp/waiting_for_license.flag

# check contents of pod
echo "Contents of data"
ls -l /data
echo "Contents of stata17"
ls -l /usr/local/stata17

cp /data/stata.lic /usr/local/stata17/stata.lic

while [ ! -f /usr/local/stata17/stata.lic ]; do sleep 1; echo "Waiting for license."; done

echo "Received a license. Starting jupyter."

start-notebook.sh $@ &

sleep 20

echo "Running Stata notebook init script."
python3 /tmp/setup_licensed_notebook.py

rm geckodriver*

echo "Init script done."
rm /usr/local/stata17/stata.lic /tmp/waiting_for_license.flag

while true; do sleep 1; done
