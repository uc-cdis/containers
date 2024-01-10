# Wait for license, start jupyter, initialize notebook, remove license

echo "Checking for license copied by sidecar"

while [ ! -f /usr/local/stata17/stata.lic ];
do
    sleep 5
    echo "Checking for license"
    if [ -f /data/stata.lic ]; then
        echo "Found license"
        cp /data/stata.lic /usr/local/stata17/stata.lic
        echo "Copied license"
    fi
done

echo "Received a license. Starting jupyter."

start-notebook.sh $@ &

sleep 20

echo "Running Stata notebook init script."
python3 /tmp/setup_licensed_notebook.py

rm geckodriver*

echo "Init script done."
rm /usr/local/stata17/stata.lic /data/stata.lic

while true; do sleep 1; done
