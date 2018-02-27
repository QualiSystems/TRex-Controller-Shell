#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.traffic.trex.client.trex_client import trex_exceptions


class TRexTrafficControlFlow(object):

    def __init__(self, trex_client, logger):
        self._logger = logger
        self._trex_client = trex_client

    def start_traffic(self, test_config, block_to_success=True, timeout=40, latency=1000):
        """ Start traffic based on provided test configuration file """

        if not test_config.startswith("./") and not test_config.startswith("/"):
            test_files_location = self._trex_client.get_trex_files_path()
            test_config = "{}/{}".format(test_files_location, test_config)

        if timeout < 40:
            self._logger.info("Start TRex timeout should be at least 40 seconds. Entered value: {}.".format(timeout))
            timeout = 40
            self._logger.info("Start TRex timeout changed to 40 seconds")

        run_params = dict(d=5, f=test_config, block_to_success=block_to_success, timeout=timeout)
        if latency:
            run_params.update(dict(l=latency))

        try:
            res = self._trex_client.start_trex(**run_params)
        except trex_exceptions.TRexError as e:
            self._logger.exception(e)
            raise Exception("One of the trex_cmd_options raised an exception at server")
        except trex_exceptions.TRexInUseError as e:
            self._logger.exception(e)
            raise Exception("TRex is already taken")
        except trex_exceptions.TRexRequestDenied as e:
            self._logger.exception(e)
            raise Exception("TRex is reserved for another user than the one trying start TRex")
        except Exception as e:
            self._logger.exception(e)
            raise Exception("Error happened during TRex start procedure")

    def stop_traffic(self, force=False):
        """ Stop traffic """

        try:
            if not force:
                self._trex_client.stop_trex()
            else:
                self._trex_client.force_kill(confirm=False)
        except trex_exceptions.TRexRequestDenied as e:
            self._logger.exception(e)
            raise Exception("TRex is running but started by another user")
        except trex_exceptions.TRexIncompleteRunError as e:
            self._logger.exception(e)
            raise Exception("TRex is running but started by another user")
        except Exception as e:
            self._logger.exception(e)
            raise Exception("Error happened during TRex termination procedure")
