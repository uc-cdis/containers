# Signal to the distributor cron job that we want a license
# touch /tmp/waiting_for_license.flag

echo "Checking for license copied by sidecar"

# if [ -f /data/stata.lic ]; then
#   mv /data/stata.lic /usr/local/stata17/stata.lic
# else
#   echo "Error: Missing license file /data/stata.lic"
#   # rm /tmp/waiting_for_license.flag
#   # exit 0
# fi

while [ ! -f /usr/local/stata17/stata.lic ];
do
    sleep 5
    echo "Checking for license"
    if [ -f /data/stata.lic ]; then
        echo "Found license"
        ls -l /data
        cp /data/stata.lic /usr/local/stata17/stata.lic
        echo "Copied license"
        ls -l /usr/local/stata17/
    fi
done

# TODO: remove this after the distribute-licenses job is disabled
# while [ ! -f /usr/local/stata17/stata.lic ]; do sleep 1; echo "Waiting for license."; done

echo "Received a license. Starting jupyter."

start-notebook.sh $@ &

sleep 20

echo "Running Stata notebook init script."
python3 /tmp/setup_licensed_notebook.py

rm geckodriver*

echo "Init script done."
rm /usr/local/stata17/stata.lic /data/stata.lic

while true; do sleep 1; done
