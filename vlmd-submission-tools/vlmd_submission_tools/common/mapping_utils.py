'''
contains mappings (both lambda functions or column mappings)
'''
from vlmd_submission_tools.common import schemas

# split array columns
def split_str_array(string,sep='|'):
    if string:
        return [s.strip() for s in string.split(sep)]
    else:
        return None

# if object within array, assign to properties
def map_keys_vals(keys,vals):
    ''' zips two lists of the same size as
    a dictionary
    '''
    return dict(zip(keys,vals))


def split_and_map(string,prop):
    '''
    splits nested stringified delimited lists
    (delimiters being | for outer and = for inner)
    and zips/maps each of the inner lists to a set
    of values (right now keys of a dictionary)
    TODO: rename function split_and_map_to_keys
    TODO: generalize to more than keys

    '''
    if string:
        keys = prop['items']['properties'].keys()
        return [
            map_keys_vals(keys,split_str_array(x,sep='='))
            for x in split_str_array(string,sep='|')
        ]
    else:
        return None


def loads_dict(string,item_sep='|',key_val_sep='='):
    if string:
        return dict([split_str_array(s,key_val_sep)
            for s in split_str_array(string,item_sep)])


def convert_rec_to_json(field):
    '''
    converts a flattened dictionary to a nested dictionary
    based on JSON path dot notation indicating nesting
    '''
    # print(f"Working on field {field}")
    field_json = {}
    for prop_path,prop in field.items():
        if prop:
            # initiate the prop to be added with the entire
            # field
            prop_json = field_json
            # get the inner most dictionary item of the jsonpath
            nested_names = prop_path.split('.')
            for i,prop_name in enumerate(nested_names):
                is_last_nested = i+1==len(nested_names)
                if prop_json.get(prop_name) and not is_last_nested:
                    prop_json = prop_json[prop_name]
                # if no object currently
                elif not is_last_nested:
                    prop_json[prop_name] = {}
                    prop_json = prop_json[prop_name]
                #assign property to inner most item
                else:
                    prop_json[prop_name] = prop

    return field_json


def mapval(v,mapping):
    v = str(v)
    if v in mapping:
        return mapping[v]
    else:
        return v


def to_bool(v):
    if v.lower() in true_values:
        return True
    elif v.lower() in false_values:
        return False
    else:
        return ""


typemap = {
    #from bacpac
    'text':'string',
    'float':'number',
    #from hemo
    'NUM':'number',
    'CHAR':'string'
}


formatmap = {
    'ISO8601':'' # NOTE: this is the default date format for frictionless so not necessary to specify
}


props = schemas.heal['data_dictionary']['properties']
    #mappings for array of dicts, arrays, and dicts


true_values = ["true","1","yes","required","y"]
false_values = ["false","0","no","not required","n"]


fieldmap = {
    'constraints.enum': lambda v: split_str_array(v),
    # 'constraints.maximum':int,
    # 'constraints.minimum':int, #TODO:need to add to schema
    # 'constraints.maxLength':int,
    'cde_id': lambda v: split_and_map(v, props['cde_id']),
    'ontology_id': lambda v: split_and_map(v, props['ontology_id']),
    'encoding':lambda v: loads_dict(v),
    'format': lambda v: mapval(v,formatmap),
    'type':lambda v: mapval(v,typemap),
    #'univar_stats.cat_marginals':lambda v: split_and_map(v, prop['univar_stats']['cat_marginals']),
    'missingValues':lambda v: split_str_array(v),
    'trueValues': lambda v: split_str_array(v),
    'falseValues':lambda v: split_str_array(v),
    # 'constraints.required': lambda v: to_bool(v),
    # TODO: add stats
}


# join mappings for json to csv

def join_iter(iterable,sep_list="|"):
    return sep_list.join([str(p) for p in iterable])


def join_dictvals(dictionary:dict,sep:str):
    return sep.join(dictionary.values())


def join_dictitems(dictionary:dict,sep_keyval='=',sep_items='|'):
    dict_list = [key+sep_keyval+val for key,val in dictionary.items()]
    return sep_items.join(dict_list)


joinmap = {
    'constraints.enum': join_iter,
    'cde_id': join_dictvals,
    'ontology_id': join_dictvals,
    'encodings': join_dictitems,
    'missingValues':join_iter,
    'trueValues': join_iter,
    'falseValues':join_iter,
    # TODO: add stats
}


def join_prop(propname,prop):
    return joinmap[propname](prop) if propname in joinmap else prop
