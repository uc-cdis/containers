# Check for license, start jupyter, initialize notebook, remove license
#
# Usage:
# wait_for_license.sh [LICENSE_NAME] [LICENSE_KEY]
#
# where
# LICENSE_NAME is the name of the environment variable with the
# stata license. Default = 'STATA_WORKSPACE_GEN3_LICENSE'.
#
# LICENSE_KEY is the name of the secret key, specified by
# license.g3auto_key in the hatchery.json. Default = 'stata_license.txt'

LICENSE_VAR="STATA_WORKSPACE_GEN3_LICENSE"
KEY_VAR="stata-license.txt"
TARGET_FILE="/usr/local/stata18/stata.lic"

echo "Checking stata license"
if [[ ! -n "${!LICENSE_VAR}" ]]; then
  echo "Exiting. Stata license is empty."
  exit 0
fi

if echo "${!LICENSE_VAR}" | grep -q "${KEY_VAR}" ; then
  echo "Found key"
else
  echo "Exiting. Environment variable does not contain key ${KEY_VAR}."
  exit 0
fi

LICENSE_DATA="${!LICENSE_VAR}"
echo ${LICENSE_DATA} | jq -r --arg k ${KEY_VAR} '.[$k]' > ${TARGET_FILE}

if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "Exiting. Did not save license."
    exit 0
fi

echo "Received a license. Starting jupyter."

start-notebook.sh $@ &

sleep 20

echo "Running Stata notebook init script."
python3 /tmp/setup_licensed_notebook.py

rm geckodriver*

echo "Init script done."
rm ${TARGET_FILE}

while true; do sleep 1; done
