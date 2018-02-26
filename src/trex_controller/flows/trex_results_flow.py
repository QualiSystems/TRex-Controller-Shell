#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

DEF_TIMEOUT = 5  # in seconds


class TRexResultsFlow(object):

    def __init__(self, trex_client, logger):
        self._logger = logger
        self._trex_client = trex_client

    def get_results(self):
        """ Get results """

        try:
            result = self._trex_client.get_result_obj()

            is_running = self._trex_client.is_running(dump_out=dict())

            # while self._trex_client.is_running(dump_out=dict()):
            while is_running:
                result = self._trex_client.get_result_obj()
                time.sleep(DEF_TIMEOUT)
                is_running = self._trex_client.is_running(dump_out=dict())
            return result
        except Exception as e:
            self._logger.exception(e)
            raise Exception("Error happened during getting TRex results")
