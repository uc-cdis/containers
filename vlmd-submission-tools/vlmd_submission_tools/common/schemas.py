from pathlib import Path
from frictionless import Schema
import json
import jsonschema

# TODO: use data_dictionary.json
# TODO: output informative error messages in validation
# NOTE: would it be good to also have a frictionless CSV template with regexs?...may be easier to spot text errors?

# can change to request.get(github)
with open('vlmd_submission_tools/common/fields.json') as f:
    data = json.load(f)

heal = {
    'data_dictionary': data
}

schema = {
    'type':'object',
    'required':[
        'title',
        'data_dictionary'
    ],
    'properties':{
        'title':{'type':'string'},
        'description':{'type':'string'},
        'data_dictionary':{'type':'array','items':heal['data_dictionary']}
    }
}
