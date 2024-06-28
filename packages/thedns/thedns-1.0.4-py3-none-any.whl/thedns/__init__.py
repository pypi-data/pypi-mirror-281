import requests
import json
from auth import _token
from auth import _credentials
from auth import _request_headers
from network import _get_private_ip
from network import _get_rr_string
from wanwang import _list_rrs
from wanwang import _build_payload
from wanwang import _update_rr

class DDNS(object):
    _service_url_dns = 'https://devnull.cn/dns'
    access_key = None
    secret_key = None
    email = None
    public_ip = None
    private_ip = None
    token = None
    request_headers = None
    def __init__(self):
        self.access_key, self.secret_key, self.email = _credentials()
        self.public_ip = requests.get('https://devnull.cn/ip').json()['origin']
        self.private_ip = _get_private_ip()
        self.token = _token(self.email, self.access_key, self.secret_key)
        self.request_headers = _request_headers(token=self.token)
        self.rr_string_public = _get_rr_string() + '.public'
        self.rr_string_private = _get_rr_string() + '.private'
    # def list_rrs(self):
    #     return _list_rrs(url='https://devnull.cn/dns', request_headers=self.request_headers)
    # def check_rr(self,rr_record=None, rr_value=None):
    #     return_data = {
    #         'exists': False,
    #         'ddns_request_type': 'create_rr_free'
    #     }
    #     rrs = _list_rrs(url='https://devnull.cn/dns', request_headers=self.request_headers)
    #     for _ in rrs:
    #         rr_value_queried = rrs[_]['rr_value']
    #         if rr_record == rrs[_]['rr_record']:
    #             if rr_value == rr_value_queried:
    #                  return_data = {
    #                      'exists': True,
    #                      'ddns_request_type': 'take_no_action',
    #                      'rr_id': _
    #                  }
    #             elif rr_value != rr_value_queried:
    #                 return_data = {
    #                     'exists': True,
    #                     'ddns_request_type': 'update_rr_free',
    #                     'rr_id': _
    #                 }
    #             break
    #     return return_data
    # def ddns_run_single_disabled(self, rr_record=None, rr_value=None):
    #     ddns_request_type = 'create_rr_free'
    #     payload_rr_id = None
    #     rrs = _list_rrs(url='https://devnull.cn/dns', request_headers=self.request_headers)
    #     rrs_reformed = dict()
    #     for _id in rrs:
    #         _record = rrs[_id]['rr_record']
    #         _value = rrs[_id]['rr_value']
    #         rrs_reformed[_record] = {
    #             '_id': _id,
    #             '_value': _value
    #         }
    #     for _rr in rrs_reformed:
    #         _value = rrs_reformed[_rr]['_value']
    #         _id = rrs_reformed[_rr]['_id']
    #         if _rr == rr_record:
    #             if _value != rr_value:
    #                 ddns_request_type = 'update_rr_free'
    #                 payload_rr_id = rrs_reformed[_rr]['_id']
    #             else:
    #                 ddns_request_type = 'take_no_action'
    #             break
    #     final_payload = _build_payload(ddns_request_type=ddns_request_type, rr_record=rr_record, rr_value=rr_value)
    #     final_payload['rr_id'] = payload_rr_id
    #     # final request to api
    #     _request = requests.post('https://devnull.cn/dns',
    #                              headers=self.request_headers,
    #                              data=json.dumps(final_payload)).json()
    def update(self):
        _update_rr(request_headers=self.request_headers, rr_record=self.rr_string_private,rr_value=self.private_ip)
        _update_rr(request_headers=self.request_headers, rr_record=self.rr_string_public,rr_value=self.public_ip)
