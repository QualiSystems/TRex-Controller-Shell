#!/usr/bin/python
# -*- coding: utf-8 -*-

from trex_controller.helpers import constants


class TrafficGeneratorControllerResource(object):
    def __init__(self, address=None, username=None, password=None, shell_name=None, attributes=None):
        """

        :param str address: IP address of the resource
        :param str shell_name: shell name
        :param str user: controller CLI user
        :param str password: controller CLI password
        :param dict[str, str] attributes: attributes of the resource
        """
        self.address = address
        self.attributes = attributes or {}
        self.username = username
        self.password = password

        if shell_name:
            self.namespace_prefix = "{}.".format(shell_name)
        else:
            self.namespace_prefix = ""

    @property
    def cli_connection_type(self):
        """

        :rtype: str
        """
        return constants.CLI_CONNECTION_TYPE

    @property
    def cli_tcp_port(self):
        """

        :rtype: str
        """
        return constants.CLI_TCP_PORT

    @property
    def sessions_concurrency_limit(self):
        """

        :rtype: float
        """
        return constants.SESSIONS_CONCURRENCY_LIMIT

    @property
    def test_files_location(self):
        """

        :rtype: float
        """
        return self.attributes.get("{}Test Files Location".format(self.namespace_prefix), "")

    @property
    def trex_daemon_port(self):
        """  """

        return self.attributes.get("{}TRex Daemon Port".format(self.namespace_prefix), constants.TREX_DAEMON_PORT)

    @staticmethod
    def _get_resource_attribute_value(resource, attribute_name):
        """

        :param resource cloudshell.api.cloudshell_api.ResourceInfo:
        :param str attribute_name:
        """
        for attribute in resource.ResourceAttributes:
            if attribute.Name.lower() == attribute_name.lower():
                return attribute.Value

    @staticmethod
    def _get_chassis_model(cs_api, reservation_id):
        """

        :param cs_api:
        :param reservation_id:
        :return:
        """
        for resource in cs_api.GetReservationDetails(reservationId=reservation_id).ReservationDescription.Resources:
            if resource.ResourceModelName in constants.CHASSIS_MODELS:
                return cs_api.GetResourceDetails(resource.Name)

        raise Exception("Unable to find {} model in the current reservation".format(constants.CHASSIS_MODELS))

    @classmethod
    def from_context(cls, context):
        """

        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :return:
        """
        return cls(attributes=dict(context.resource.attributes))

    @classmethod
    def create_from_chassis_resource(cls, context, cs_api):
        """Create an instance of TrafficGeneratorControllerResource from the given context

        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param cs_api:
        :rtype: TrafficGeneratorControllerResource
        """
        reservation_id = context.reservation.reservation_id
        chassis_resource = cls._get_chassis_model(cs_api=cs_api, reservation_id=reservation_id)
        username = cls._get_resource_attribute_value(resource=chassis_resource, attribute_name="User")
        password = cs_api.DecryptPassword(cls._get_resource_attribute_value(resource=chassis_resource,
                                                                            attribute_name="Password")).Value

        return cls(address=chassis_resource.FullAddress,
                   username=username,
                   password=password,
                   attributes=dict(context.resource.attributes))
