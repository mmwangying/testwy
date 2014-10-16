#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2014-10-08 16:42
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import unittest
import sys
sys.path.append('./')
import testReportService
import testCampaignService
import testRPTAdgroup
import MTextTestRunner
import settings
import datetime

alltests = unittest.TestSuite([testRPTAdgroup.alltests\
                               #, testCampaignService.alltests\
                               #, testReportService.alltests\
                               ])
if __name__ == "__main__":
    if settings.NeedLog:
        fb = file('./report/report_%s.html'%datetime.date.today(),'wb')
        mrunner = MTextTestRunner.TextTestRunner(stream=fb,title='The Result Of Unit Test',description='The first run')
    else:
        mrunner = MTextTestRunner.TextTestRunner()
    mrunner.run(alltests)
    #unittest.main(testRunner = mrunner)
