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


@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test")
class TestCampaignService(unittest.TestCase):

    '''Campaign Service Test'''

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_campaign_1(self):
        pass

    def test_campaign_2(self):
        self.assertEqual(1+1, 2.1)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

alltests = unittest.TestLoader().loadTestsFromTestCase(TestCampaignService)

#if __name__ == "__main__":
#    mrunner = MTextTestRunner.TextTestRunner()
#    #mrunner.run(alltests)
#    unittest.main(testRunner = mrunner)
