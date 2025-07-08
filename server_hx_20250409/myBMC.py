import argparse
import os
import pdb
from redfish import redfish_client
import myformat as mf
import sys
import logging
from mytools import *


class BMC:
    """
    BMC base class for the different BMC　Vendor
    """

    def __init__(self,args):
        self.host = args.host
        self.username = args.username
        self.password = args.password
        self.url = 'https://' + self.host
        self.client = redfish_client(base_url=self.url, username=self.username, password=self.password)
        self.client.login()



    def get_redfish_contents(self,url):
        """get the dict from the redfish url"""
        return self.client.get(url).dict


    def get_redfish_urls(self,url):
        """
        get the url list for the detail items
        """
        pass




