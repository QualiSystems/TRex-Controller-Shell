#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.traffic.trex.cli.trex_cli_handler import TRexCliHandler
from trex_controller.flows.download_server_config_flow import TRexDownloadServerConfigFlow
from trex_controller.flows.upload_server_config_flow import TRexUploadServerConfigFlow


class TRexServerConfigurationRunner(object):
    def __init__(self, cli, resource_config, logger):
        self._cli = cli
        self._resource_config = resource_config
        self._logger = logger

    @property
    def cli_handler(self):
        """ CLI Handler property """

        return TRexCliHandler(self._cli,
                              self._resource_config.address,
                              self._resource_config.username,
                              self._resource_config.password)

    @property
    def upload_trex_server_config_flow(self):
        """  """
        return TRexUploadServerConfigFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def download_trex_server_config_flow(self):
        """  """

        return TRexDownloadServerConfigFlow(cli_handler=self.cli_handler, logger=self._logger)

    def upload_trex_server_config(self, server_config_url):
        """ Upload Cisco TRex Server configuration to FTP/TFTP Server """

        return self.upload_trex_server_config_flow.execute_flow(trex_config_url=server_config_url)

    def download_trex_server_config(self, server_config_url):
        """ Download Cisco TRex Server configuration from FTP/TFTP Server """

        return self.download_trex_server_config_flow.execute_flow(trex_config_url=server_config_url)
