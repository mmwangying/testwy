#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 16:36
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""


import unittest
import settings
import MTextTestRunner
from mock import Mock, patch
from common import CommonLib
import random

import sys
import os
sys.path.append('../../comm_lib/')
sys.path.append('../')
import settings
import datetime
import logging
import logging.config
from report_db.conf import set_env
set_env.getEnvReady()
logging.config.fileConfig('../report_db/conf/consolelogger.conf')

from report_db.services.adgroup_rpt_search_service import AdgroupRptSearchService
from report_db.Libs.date_handle import DateHandle
from tao_models.simba_rpt_campadgroupeffect_get import SimbaRptCampadgroupEffectGet 
from tao_models.simba_rpt_campadgroupbase_get import SimbaRptCampadgroupBaseGet 
#from tao_models import simba_rpt_adgroupbase_get
#from tao_models import simba_rpt_adgroupeffect_get

from api_server.conf.settings import set_api_source
from shop_db.services.shop_info_service import ShopInfoService

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test")
class TestRPTAdgroupService(unittest.TestCase):

    '''Campaign Service Test'''

    @classmethod
    def setUpClass(cls):
        set_api_source('unit-test')
        cls.testdata = [{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':True, 'last_date':-8, 's_offset':-7, 'e_offset':-7, 'tc_info':'datetime.now()小于8点，last_date是30天内（15天内）,获取昨天的数据'}]
        #cls.testdata = [{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':False, 'last_date':-7, 's_offset':-1, 'e_offset':-1, 'tc_info':'datetime.now()小于8点，last_date是30天内（15天内）,获取昨天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':False, 'last_date':-7, 's_offset':-7, 'e_offset':-1, 'tc_info':'datetime.now()小于8点，last_date是30天内（15天内）,获取过去7天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':False, 'last_date':-7, 's_offset':-15, 'e_offset':-1, 'tc_info':'datetime.now()小于8点，last_date是30天内（15天内）,获取过去15天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':False, 'last_date':32, 's_offset':-1, 'e_offset':-1, 'tc_info':'datetime.now()小于8点，last_date是30天外,获取昨天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':False, 'last_date':32, 's_offset':-7, 'e_offset':-1, 'tc_info':'datetime.now()小于8点，last_date是30天外,获取过去7天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':False, 'last_date':32, 's_offset':-15, 'e_offset':-1, 'tc_info':'datetime.now()小于8点，last_date是30天外,获取过去15天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':True, 'last_date':-7, 's_offset':-1, 'e_offset':-1, 'tc_info':'datetime.now()大于8点，last_date是30天内（15天内）,获取昨天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':True, 'last_date':-7, 's_offset':-7, 'e_offset':-1, 'tc_info':'datetime.now()大于8点，last_date是30天内（15天内）,获取过去7天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':True, 'last_date':-7, 's_offset':-15, 'e_offset':-1, 'tc_info':'datetime.now()大于8点，last_date是30天内（15天内）,获取过去15天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':True, 'last_date':32, 's_offset':-1, 'e_offset':-1, 'tc_info':'datetime.now()大于8点，last_date是30天外,获取昨天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':True, 'last_date':32, 's_offset':-7, 'e_offset':-1, 'tc_info':'datetime.now()大于8点，last_date是30天外,获取过去7天的数据'},
                        #{'nick':u'晓迎', 'campaign_id':7155359, 'adgroup_id':413379620, 'need_instant': True, 'over_8':True, 'last_date':32, 's_offset':-15, 'e_offset':-1, 'tc_info':'datetime.now()大于8点，last_date是30天外,获取过去15天的数据'}]

    def setUp(self):
        pass
        #self.tclass = AdgroupRptSearchService

    @patch('report_db.services.adgroup_rpt_search_service.ShopRptInfo')
    @patch('report_db.services.adgroup_rpt_search_service.date_now')
    #@patch('report_db.services.adgroup_rpt_search_service.datetime')
    def test_rpt_adgroup(self, mock_datetime, mock_ShopRptInfo):
    #def test_rpt_adgroup(self):
        fields = {'base':True,'effect':True}
        for data in self.testdata:
            date_now = datetime.datetime.now()
            nick = data['nick']
            shop_info = ShopInfoService.get_shop_info_by_nick('SYB', nick)
            sid = shop_info['sid']
            start_date = date_now + datetime.timedelta(data['s_offset'])
            end_date = date_now + datetime.timedelta(data['e_offset'])
            need_instant = data['need_instant']
            campaign_id = data['campaign_id']
            adgroup_id = data['adgroup_id']
            over_8 = data['over_8']
            last_date = date_now + datetime.timedelta(data['last_date'])

            if over_8:
                hour = random.randint(8,23)
                #mock_datetime.datetime.now.return_value = datetime.datetime(date_now.year, date_now.month, date_now.day, hour, 10, 38, 665147)
                mock_datetime = datetime.datetime(date_now.year, date_now.month, date_now.day, hour, 10, 38, 665147)
            else:
                hour = random.randint(0,7)
                #mock_datetime.datetime.now.return_value = datetime.datetime(date_now.year, date_now.month, date_now.day, hour, 10, 38, 665147)
                mock_datetime = datetime.datetime(date_now.year, date_now.month, date_now.day, hour, 10, 38, 665147)
            mock_ShopRptInfo.get_adgroups_rpt_last_modified_date.return_value = last_date
            
            search_info = {'nick':nick,'sid':sid,'campaign_id':campaign_id}

            date_list = DateHandle.get_date_list_from_date(start_date, end_date)
            actual_result = AdgroupRptSearchService.adgroup_rpt_search(sid, [adgroup_id], start_date, end_date, fields, need_instant, search_info)
            actual_result = CommonLib.round_rpt(actual_result)

            #expect_result_base = simba_rpt_adgroupbase_get.SimbaRptAdgroupBaseGet.get_rpt_adgroupbase_list(nick, campaign_id, adgroup_id, start_date, end_date, 'SEARCH, CAT, NOSEARCH', 'SUMMARY')
            expect_result_base_list = SimbaRptCampadgroupBaseGet.get_rpt_adgroupbase_list(nick, campaign_id, start_date, end_date, 'SEARCH,CAT,NOSEARCH', 'SUMMARY')
            for item in expect_result_base_list:
                if item['adgroupid'] == adgroup_id:
                    expect_result_base.append(item)
            #expect_result_effect = simba_rpt_adgroupeffect_get.SimbaRptAdgroupEffectGet.get_rpt_adgroupeffect_list(nick, campaign_id, adgroup_id, start_date, end_date, 'SEARCH, CAT, NOSEARCH', 'SUMMARY')
            expect_result_effect_list = SimbaRptCampadgroupEffectGet.get_rpt_adgroupeffect_list(nick, campaign_id, start_date, end_date, 'SEARCH,CAT,NOSEARCH', 'SUMMARY')
            for item in expect_result_effect_list:
                if item['adgroupid'] == adgroup_id:
                    expect_result_effect.append(item)

            expect_result_base = CommonLib.fill_rpt_zero(date_list,  expect_result_base, nick, 'base', "adgroup", sid, adgroup_id)
            expect_result_effect = CommonLib.fill_rpt_zero(date_list, expect_result_effect, nick, 'effect', "adgroup", sid, adgroup_id)

            count = len(expect_result_base)
            self.assertEqual(len(actual_result),len(expect_result_base), "base返回数据条数不对")
            self.assertEqual(len(actual_result),len(expect_result_effect), "base返回数据条数不对")
            try:
                for index in range(count):
                    self.assertEqual(actual_result[index]['base'],expect_result_base[index])
                    self.assertEqual(actual_result[index]['effect'],expect_result_effect[index])
            except:
                self.assertTrue(False,data['tc_info'])

    @unittest.skip("Program Test")
    def test_try(self):
        self.assertEqual(1+1, 2.1)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

alltests = unittest.TestLoader().loadTestsFromTestCase(TestRPTAdgroupService)

#if __name__ == "__main__":
#    mrunner = MTextTestRunner.TextTestRunner()
#    #mrunner.run(alltests)
#    unittest.main(testRunner = mrunner)
