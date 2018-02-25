#!/usr/bin/python
# -*- coding: utf-8 -*-

from trex_controller.actions.trex_test_actions import TRexTestActions


class TRexLoadTestConfigFlow(object):

    def __init__(self, cli_handler, trex_client, logger):
        self._logger = logger
        self._cli_handler = cli_handler
        self._trex_client = trex_client

    def load_test_config(self, test_config_path):
        """ Load test configuration files from FTP/TFTP Server or Execution Server"""

        if test_config_path.lower().startswith("ftp") or test_config_path.lower().startswith("tftp"):
            with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
                config_actions = TRexTestActions(enable_session, self._trex_client, self._logger)

                config_actions.download_file(test_config_url=test_config_path)
        else:
            self._trex_client.push_files(test_config_path)
