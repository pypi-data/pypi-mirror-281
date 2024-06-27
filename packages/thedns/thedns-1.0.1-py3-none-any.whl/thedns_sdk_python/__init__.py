import time
import requests
import json
import configparser
import hashlib
import pathlib
import socket

## to remove pydig as the cache leads to all kinds of shit.
# import pydig



service_url_dns = "https://devnull.cn/dns"
auth_url = 'https://devnull.cn/identity'
anonymous_accesskey = 'Eo3YeVIcJzUCUgs2so8qb7pt'
anonymous_secretkey = '8LmdaD0MPen7mPkrDa4F97oW'
domain = 'thedns.cn'



def configfile():
    config_dir = pathlib.Path.home() / '.devnull'
    pathlib.Path(config_dir).mkdir(parents=True, exist_ok=True)
    return config_dir / 'credentials'

def my_token(auth_url=auth_url):
    resource_type = 'token'
    try:
        _c = configfile()
        with _c.open('r') as f:
            config = configparser.ConfigParser()
            config.read_file(f)
            accesskey = config['default']['accesskey']
            secretkey = config['default']['secretkey']
            email = config['default']['email']
    except:
        accesskey = anonymous_accesskey
        secretkey = anonymous_secretkey
        email = 'ddns-free@thedns.cn'
    # print(accesskey, secretkey, email)
    hashed_accesskey = hashlib.sha256(accesskey.encode()).hexdigest()
    hashed_secretkey = hashlib.sha256(secretkey.encode()).hexdigest()
    hashed_email = hashlib.md5(email.encode()).hexdigest()
    _plain = hashed_accesskey + hashed_secretkey
    _password = hashlib.sha256(_plain.encode()).hexdigest()
    # print(_password)
    data = json.dumps({
        'email': email,
        'checksum': hashed_email,
        'accesskey': accesskey,
        'password': _password,
        'resource_type': resource_type
    })
    # print(data)
    headers = {'Content-Type': 'application/json'}
    responsed_token = requests.post(auth_url, data=data, headers=headers)
    _ = responsed_token.json()
    # print(_)
    token_string = 'Bearer ' + _['token']
    return token_string
    # except:
    #     return 'failed_to_generate_an_token'


def request_headers():
    return {
        'Authorization': my_token(auth_url),
        'Content-Type': 'application/json'
    }

def get_rr_string():
    try:
        with open('/etc/machine-id', 'r') as f:
            rr_string = hashlib.md5(f.read().encode()).hexdigest()
    except:
        rr_string = hashlib.md5(socket.gethostname().encode()).hexdigest()
    return rr_string

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    private_ip_string = s.getsockname()[0]
    s.close()
    return private_ip_string

def get_public_ip():
    r = requests.get('https://devnull.cn/ip')
    return r.json()['origin']



def check_rr_exists(rr_record=None):
    return_data = {
        'exists': False
    }
    rrs = list_rrs()
    for _ in rrs:
        if rr_record == rrs[_]['rr_record']:
            rr_value_queried = rrs[_]['rr_value']
            return_data = {
                'exists': True,
                'rr_value_queried': rr_value_queried,
                'rr_id': _
            }
            break
    return return_data


def get_request_type(rr_record=None, rr_value=None):
    _exists = check_rr_exists(rr_record=rr_record)
    if not _exists['exists']:
        return 'create_rr_free'
    elif _exists['exists'] and rr_value not in _exists['rr_value_queried']:
        return 'update_rr_free'
    else:
        return 'take_no_action'

def list_rrs():
    payload = json.dumps({
        "action_type": 'list_rrs_free',
    })
    _response_list_rrs = requests.request("POST", service_url_dns, headers=request_headers(), data=payload).json()
    # print(f"Listing RRs: {_response_list_rrs}")
    return _response_list_rrs

def ddns():
    rrs = list_rrs()
    existing_rrs_reformed = dict()
    for rr_id in rrs:
        rr_record = rrs[rr_id]['rr_record']
        rr_value = rrs[rr_id]['rr_value']
        existing_rrs_reformed[rr_record] = {
            'rr_id': rr_id,
            'rr_value': rr_value
        }
    _raw = dict()
    _returned_data = dict()
    rr_record_short = get_rr_string()
    rr_string_private = rr_record_short + '.private'
    rr_string_public = rr_record_short + '.public'
    private_fqdn = rr_string_private + '.' + domain
    public_fqdn = rr_string_public + '.' + domain
    rr_value_private = get_private_ip()
    rr_value_public = get_public_ip()
    _raw[private_fqdn] = {
        'rr_record': rr_string_private,
        'rr_value': rr_value_private,
    }
    _raw[public_fqdn] = {
        'rr_record': rr_string_public,
        'rr_value': rr_value_public,
    }
    print(f"raw data: {_raw}")
    # check the existence first by reading listing_rrs
    print(f"Processing for your system: {rr_record_short}")
    for _ in _raw.keys():
        rr_record = _raw[_]['rr_record']
        rr_value = _raw[_]['rr_value']
        api_request_type = get_request_type(rr_record=rr_record, rr_value=rr_value)
        payload_data = {
            "action_type": api_request_type,
            "rr_type": 'A',
            "rr_record": rr_record,
            "rr_value": rr_value,
        }
        if api_request_type == 'update_rr_free':
            payload_data['rr_id'] = existing_rrs_reformed[rr_record]['rr_id']
        print(f"Payload: {payload_data}")
        _request = requests.request("POST", service_url_dns, headers=request_headers(), data=json.dumps(payload_data)).json()
        print(f"Response from API: {_request}")
        _returned_data[_] = _raw[_]['rr_value']
        time.sleep(2)
    return _returned_data

