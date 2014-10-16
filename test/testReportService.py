#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 14:07
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys
import os
sys.path.append('../../comm_lib/')
sys.path.append('../')
import settings
import datetime
import logging
import logging.config
import unittest
#from MTextTestRunner import TextTestRunner

from report_db.conf import set_env
set_env.getEnvReady()
logging.config.fileConfig('../report_db/conf/consolelogger.conf')

from report_db.services import cust_rpt_search_service
from report_db.services import campaign_rpt_search_service

from report_db.Libs.date_handle import DateHandle
from tao_models import simba_rpt_custbase_get
from tao_models import simba_rpt_custeffect_get

from tao_models import simba_rpt_campaignbase_get
from tao_models import simba_rpt_campaigneffect_get

from api_server.conf.settings import set_api_source
from shop_db.services.shop_info_service import ShopInfoService

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestReportService(unittest.TestCase):
    '''Report Service Test'''
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        set_api_source('unit-test')
        
        cls.testdata1 = [{'nick':'晓迎', 'need_instant':'True', 's_offset':-1, 'e_offset':-1, 'tc_info':'调API，昨天'},
                        {'nick':'晓迎', 'need_instant':'True', 's_offset':-7, 'e_offset':-1, 'tc_info':'调API，过去7天'},
                        {'nick':'晓迎', 'need_instant':'True', 's_offset':-15, 'e_offset':-1, 'tc_info':'调API，过去15天'},
                        {'nick':'晓迎', 'need_instant':'True', 's_offset':-30, 'e_offset':-1, 'tc_info':'调API，过去30天'},
                        {'nick':'晓迎', 'need_instant':'True', 's_offset':-1, 'e_offset':-15, 'tc_info':'调API，起止日期反序'},
                        {'nick':'晓迎', 'need_instant':'True', 's_offset':-15, 'e_offset':1, 'tc_info':'调API，截止日期超过昨天'},
                        {'nick':'晓迎', 'need_instant':'True', 's_offset':-15, 'e_offset':-2, 'tc_info':'调API，正常范围'}]

        cls.testdata2 = [{'nick':'晓迎', 'campaignid':7155359, 'need_instant':'True', 's_offset':-1, 'e_offset':-1, 'tc_info':'调api，昨天'},
                         {'nick':'晓迎', 'campaignid':7155359, 'need_instant':'True', 's_offset':-7, 'e_offset':-1, 'tc_info':'调api，过去7天'},
                         {'nick':'晓迎', 'campaignid':7155359, 'need_instant':'True', 's_offset':-15, 'e_offset':-1, 'tc_info':'调api，过去15天'},
                         {'nick':'晓迎', 'campaignid':7155359, 'need_instant':'True', 's_offset':-30, 'e_offset':-1, 'tc_info':'调api，过去30天'},
                         {'nick':'晓迎', 'campaignid':7155359, 'need_instant':'True', 's_offset':-1, 'e_offset':-15, 'tc_info':'调API，起止日期反序'},
                         {'nick':'晓迎', 'campaignid':7155359, 'need_instant':'True', 's_offset':-15, 'e_offset':1, 'tc_info':'调API，截止日期超过昨天'},
                         {'nick':'晓迎', 'campaignid':7155359, 'need_instant':'True', 's_offset':-15, 'e_offset':-2, 'tc_info':'调API，正常范围'}]

    def setUp(self):
        self.tclass1 = cust_rpt_search_service.CustRptSearchService()
        self.tclass2 = campaign_rpt_search_service.CampaignRptSearchService()

    def shop_report_cont(self, date_list,rpt_list,nick,rpt_type,sid):
        if len(date_list) == len(rpt_list):
            return rpt_list
        for index in range(len(date_list)):
            if date_list[index] == rpt_list[index]['date']:
                continue
            if rpt_type == 'base':
                rpt_zero = {"aclick" : 0, "cpm" : 0.0, "ctr" :0.0, "source" : "summary", "cpc" : 0.0, "nick" :nick, "cost" : 0,  
                            "date" : date_list[index], "impressions" : 0, "click" : 0, "sid": sid}
            else:
                rpt_zero = {"favshopcount" : 0,"directpay" : 0,"source" : "summary","indirectpay" : 0,"nick" : nick,"favitemcount" : 0,
                            "indirectpaycount" : 0,"date" : date_list[index],"directpaycount" : 0, "sid": sid}
            rpt_list.insert(index,rpt_zero)
        return rpt_list
    #对api获取的camp报表中缺失的部分补零，满足比较的条件   
    def camp_report_cont(self,date_list,rpt_list,nick,rpt_type,sid,campaign_id):
        if len(date_list) == len(rpt_list):
            return rpt_list
        for index in range(len(date_list)):
            if date_list[index] == rpt_list[index]['date']:
                continue
            if rpt_type == 'base':
                rpt_zero = {"aclick": 0, "avgpos":0.0, "campaignid":campaign_id,
                            "click":0, "cost":0, "cpc":0.0, "cpm":0.0, "ctr":0.0,
                            "date": date_list[index], "impressions":0, "nick":nick,
                            "searchtype":"summary", "sid":sid, "source":"summary"}
            else:
                rpt_zero = {"campaignid":campaign_id, "date":date_list[index], 
                            "directpay":0, "directpaycount":0, "favitemcount":0,
                            "favshopcount":0, "indirectpay":0, "indirectpaycount":0,
                            "nick":nick, "searchtype":"summary", "sid":sid, "source":"summary"}
            rpt_list.insert(index,rpt_zero)
        return rpt_list
    #对接口返回数据的精度进行修改方便比较，去掉不需要的aclick
    def round_camp_rpt(self, rpt_list, fields):
        for rpt in rpt_list:
            if fields['base']:
                rpt['base'].pop('aclick')
                rpt['base']['avgpos'] = int(round(rpt['base']['avgpos'],2))
                rpt['base']['cpc'] = int(round(rpt['base']['cpc'],2))
                rpt['base']['cpm'] = int(round(rpt['base']['cpm'],2))
                rpt['base']['ctr'] = int(round(rpt['base']['ctr'],2))
        return rpt_list
    #对api返回数据的精度进行修改方便比较，去掉不需要的aclick
    def deAclick(self,rpt_list):
        for rpt in rpt_list:
            rpt.pop('aclick')
            rpt['avgpos'] = int(round(rpt['avgpos'],2))
            rpt['cpc'] = int(round(rpt['cpc'],2))
            rpt['cpm'] = int(round(rpt['cpm'],2))
            rpt['ctr'] = int(round(rpt['ctr'],2))
        return rpt_list

    @unittest.skip("Unconditionally skip the decorated test")
    def test_skip(self):
        """test"""
        pass

    @unittest.expectedFailure
    def test_expectedFailure(self):
        """test"""
        print self.testdata

    def test_shop_rpt_search(self):
        """test"""
        fields = {'base':True, 'effect':True}
        date_now = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
        
        for data in self.testdata1:
            nick = data['nick']
            shop_info = ShopInfoService.get_shop_info_by_nick('SYB',nick)
            access_token = shop_info['access_token']
            subway_token = shop_info['subway_token']
            token = {'access_token': shop_info['access_token'], 'subway_token': shop_info['subway_token']}
            sid = shop_info['sid']
            start_date = date_now + datetime.timedelta(data['s_offset'])
            end_date = date_now + datetime.timedelta(data['e_offset'])
            need_instant = data['need_instant']
            
            actual_result = self.tclass1.shop_rpt_search(nick, sid, start_date, end_date, fields,
                                                        need_instant, token)
            
            if start_date > end_date or end_date > date_now:
                try:
                    self.assertEqual(actual_result,[])
                except:
                    self.assertTrue(False,data['tc_info'])
                continue

            expect_result_base = simba_rpt_custbase_get.SimbaRptCustbaseGet.get_shop_rpt_base(nick, start_date, end_date)
            expect_result_effect = simba_rpt_custeffect_get.SimbaRptCusteffectGet.get_shop_rpt_effect(nick, start_date, end_date)

            date_list = DateHandle.get_date_list_from_date(start_date, end_date)
            expect_result_base = self.shop_report_cont(date_list, expect_result_base, nick, 'base', sid)
            expect_result_effect = self.shop_report_cont(date_list, expect_result_effect, nick, 'effect', sid)
            
            count = len(expect_result_base)
            try:
                for index in range(count):
                    self.assertEqual(actual_result[index]['base'],expect_result_base[index])
                    self.assertEqual(actual_result[index]['effect'],expect_result_effect[index])
            except:
                self.assertTrue(False,data['tc_info'])


    def test_single_camp_rpt_search(self):
        """test"""
        fields = {'base':True, 'effect':True}
        date_now = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
        for data in self.testdata2:                                               
            campaign_id = data['campaignid']
            nick = data['nick']                                                  
            shop_info = ShopInfoService.get_shop_info_by_nick('SYB',nick)        
            access_token = shop_info['access_token']                             
            subway_token = shop_info['subway_token']                             
            sid = shop_info['sid']                                               
            start_date = date_now + datetime.timedelta(data['s_offset'])         
            end_date = date_now + datetime.timedelta(data['e_offset'])           
            need_instant = data['need_instant']
            search_info = {'nick':nick, 'access_token': shop_info['access_token'], 
                           'subway_token': shop_info['subway_token'], 'sid':sid}
            
            actual_result = self.tclass2.single_camp_rpt_search(campaign_id, nick, sid, start_date, end_date, fields, 
                                                                need_instant, search_info, "summary")
            
            if start_date > end_date or end_date > date_now:
                try:
                    self.assertEqual(actual_result,[])
                except:
                    self.assertTrue(False,data['tc_info'])
                continue
            
            actual_result = self.round_camp_rpt(actual_result, fields)
            expect_result_base = simba_rpt_campaignbase_get.SimbaRptCampaignbaseGet.get_camp_rpt_list_by_date(nick, campaign_id,'SUMMARY', 
                                                                                                              'SUMMARY', start_date, end_date)      
            expect_result_effect = simba_rpt_campaigneffect_get.SimbaRptCampaigneffectGet.get_camp_rpt_list_by_date(nick, campaign_id, 'SUMMARY', 
                                                                                                                   'SUMMARY', start_date, end_date)
            
            date_list = DateHandle.get_date_list_from_date(start_date,end_date)
            expect_result_base = self.camp_report_cont(date_list, expect_result_base, nick, 'base', sid,campaign_id)
            expect_result_effect = self.camp_report_cont(date_list,expect_result_effect,nick, 'effect',sid,campaign_id)
            expect_result_base = self.deAclick(expect_result_base)

            
            count = len(expect_result_base)
            try:
                for index in range(count):
                    self.assertEqual(actual_result[index]['base'],expect_result_base[index])
                    self.assertEqual(actual_result[index]['effect'],expect_result_effect[index])
            except:
                self.assertTrue(False,data['tc_info'])

        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

#custtests = unittest.TestSuite(map(TestReportService, ['test_rpt_cust_1']))
alltests = unittest.TestLoader().loadTestsFromTestCase(TestReportService)
