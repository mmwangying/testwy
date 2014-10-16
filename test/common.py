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
import datetime
import copy

class CommonLib:
    '''Common Lib'''

    '''对接口返回数据的精度进行修改方便比较，去掉不需要的aclick'''
    @classmethod
    def round_rpt(cls, rpt_list):
        for rpt in rpt_list:
            if 'aclick' in rpt['base'].keys():
                rpt['base'].pop('aclick')
            if rpt['base']['avgpos'] == 0:
                rpt['base']['avgpos'] = 0
            else:
                rpt['base']['avgpos'] = round(rpt['base']['avgpos'],2)
            if rpt['base']['cpc'] == 0:
                rpt['base']['cpc'] = 0
            else:
                rpt['base']['cpc'] = round(rpt['base']['cpc'],2)
            if rpt['base']['cpm'] == 0:
                rpt['base']['cpm']= 0
            else:
                rpt['base']['cpm'] = int(round(rpt['base']['cpm'],2))
            if rpt['base']['ctr'] == 0:
                rpt['base']['ctr'] = 0
            else:
                rpt['base']['ctr'] = round(rpt['base']['ctr'],2)
        return rpt_list

    '''对api获取的camp报表中缺失的部分补零，满足比较的条件'''
    @classmethod
    def fill_rpt_zero(cls, date_list, rpt_list, nick, rpt_type, fill_type,  sid, adgropcampaignid):
        date_l = []
        for item in date_list:
            date_rpt = datetime.datetime(item.year, item.month, item.day, 0, 0)
            date_l.append(date_rpt)
        date_list = copy.copy(date_l)
        for item in rpt_list:
            if 'sid' in item.keys():
                item.pop('sid')
            date_rpt = datetime.datetime(item['date'].year, item['date'].month, item['date'].day, 0, 0)
            if date_rpt in date_l:
                date_l.remove(date_rpt)
        if len(date_list) == len(rpt_list):
            return rpt_list
        for index in range(len(date_l)):
            if rpt_type == 'base':
                if fill_type == "adgroup":
                    rpt_zero = {"avgpos" : 0,"adgroupid" : adgropcampaignid, "searchtype" : "summary",
                                "ctr" : 0, "cpc" : 0,"cost" : 0,"source" : "summary","date" : date_l[index],
                                "impressions" : 0,"click" : 0,"cpm" : 0}
                else:
                    rpt_zero = {"aclick": 0, "avgpos":0.0, "campaignid":adgropcampaignid,
                                "click":0, "cost":0, "cpc":0.0, "cpm":0.0, "ctr":0.0,
                                "date": date_l[index], "impressions":0, "nick":nick,
                                "searchtype":"summary", "sid":sid, "source":"summary"}
            else:
                if fill_type == "adgroup":
                    rpt_zero = {"favshopcount": 0, "directpay": 0, "indirectpay":0, "searchtype" : "summary"
                                ,"favitemcount" : 0,"source" : "summary", "date" : date_l[index],
                                "directpaycount": 0, "indirectpaycount": 0,"adgroupid" : adgropcampaignid}
                else:
                    rpt_zero = {"campaignid":adgropcampaignid, "date":date_l[index],
                                "directpay":0, "directpaycount":0, "favitemcount":0,
                                "favshopcount":0, "indirectpay":0, "indirectpaycount":0,
                                "nick":nick, "searchtype":"summary", "sid":sid, "source":"summary"}
            rpt_list.insert(date_list.index(date_l[index]), rpt_zero)
        return rpt_list

    '''对api返回数据的精度进行修改方便比较，去掉不需要的aclick'''
    @classmethod
    def deleteParam(self,rpt_list):
        for rpt in rpt_list:
            rpt.pop('campaignid')
            rpt.pop('cpc')
            rpt.pop('nick')
            rpt['avgpos'] = int(round(rpt['avgpos'],2))
            rpt['cpc'] = int(round(rpt['cpc'],2))
            rpt['cpm'] = int(round(rpt['cpm'],2))
            rpt['ctr'] = int(round(rpt['ctr'],2))
        return rpt_list
