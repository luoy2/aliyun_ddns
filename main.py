import requests
import json
import logging
import logging.handlers
import os

from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest

KEY_FILE_NAME = 'key.json'


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory, mode=0o777)


class DNS(object):
    logging.basicConfig(level=0)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ensure_dir('logs/')
    fh = logging.handlers.RotatingFileHandler('logs/aliyun_ddns_record.log',
                                                          mode='a',
                                                          maxBytes=10 * 1024 * 1024,
                                                          backupCount=10)
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    def __init__(self):
        with open(KEY_FILE_NAME, 'r') as f:
            self.s = json.loads(f.read())[0]
        self.clt = client.AcsClient(self.s['AccessKeyId'], self.s['AccessKeySecret'])
        self.dns_domain, self.rc_format = self.s['rc_domain'], self.s['rc_format']

    def check_records(self):
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_DomainName(self.dns_domain)
        request.set_accept_format(self.rc_format)
        result = self.clt.do_action_with_exception(request)
        result = result.decode()
        result_dict = json.JSONDecoder().decode(result)
        result_list = result_dict['DomainRecords']['Record']
        for j in result_list:
            self.logger.info('Subdomain：' + j['RR'] + ' ' + '| RecordId：' + j['RecordId'])
            if j['RR'] == 'usdb':
                rc_rr, rc_type, rc_value, rc_record_id, rc_ttl = j['RR'], j[
                    'Type'], j['Value'], j['RecordId'], j['TTL']
                return (rc_rr, rc_type, rc_value, rc_record_id, rc_ttl)
        return ([None] * 5)




    def getMyIp(self):
        try:
            u = requests.get('https://api.ipify.org/?format=text')
            return u.text
        except requests.HTTPError as e:
            self.logger.exception('getMyIp:' + str(e))
            return None


    def update_dns(self, rc_rr, rc_type, rc_value, rc_record_id, rc_ttl):
        self.logger.info('about to update ip : {}'.format(rc_value))
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_RR(rc_rr)
        request.set_Type(rc_type)
        request.set_Value(rc_value)
        request.set_RecordId(rc_record_id)
        request.set_TTL(rc_ttl)
        request.set_accept_format(self.rc_format)
        result = self.clt.do_action_with_exception(request)
        self.logger.info(result)



    def worker(self):
        rc_rr, rc_type, rc_value, rc_record_id, rc_ttl = self.check_records()
        cur_ip = self.getMyIp()
        if cur_ip != rc_value:
            self.update_dns(rc_rr, rc_type, cur_ip, rc_record_id, rc_ttl)




if __name__ =='__main__':
    d = DNS()
    d.worker()

