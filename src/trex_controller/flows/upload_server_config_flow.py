#!/usr/bin/python
# -*- coding: utf-8 -*-

from trex_controller.actions.trex_server_config_actions import TRexServerConfigActions


class TRexUploadServerConfigFlow(object):

    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger

    def execute_flow(self, trex_config_url):
        """ Upload Cisco TRex Server configuration to FTP/TFTP Server
        :param trex_config_url: URL path

        """

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
            config_actions = TRexServerConfigActions(enable_session, self._logger)

            config_actions.upload_file(server_config_url=trex_config_url)
