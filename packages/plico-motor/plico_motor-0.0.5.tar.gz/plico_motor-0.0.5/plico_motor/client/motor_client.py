#!/usr/bin/env python
from plico_motor.client.abstract_motor_client import AbstractMotorClient
from plico.rpc.abstract_remote_procedure_call import \
    AbstractRemoteProcedureCall
from plico.utils.logger import Logger
from plico.utils.decorator import override, returns
from plico.utils.snapshotable import Snapshotable
from plico.client.serverinfo_client import ServerInfoClient
from plico.client.hackerable_client import HackerableClient
from plico_motor.types.motor_status import MotorStatus
from plico_motor.utils.timeout import Timeout


class MotorClient(AbstractMotorClient,
                  HackerableClient,
                  ServerInfoClient):

    def __init__(self,
                 rpcHandler,
                 sockets,
                 axis=1):
        assert isinstance(rpcHandler, AbstractRemoteProcedureCall)

        self._rpcHandler = rpcHandler
        self._requestSocket = sockets.serverRequest()
        self._statusSocket = sockets.serverStatus()
        self._logger = Logger.of('Motor client')
        self._axis = axis
        HackerableClient.__init__(self,
                                  self._rpcHandler,
                                  self._requestSocket,
                                  self._logger)
        ServerInfoClient.__init__(self,
                                  self._rpcHandler,
                                  self._requestSocket,
                                  self._logger)

    @override
    @returns(MotorStatus)
    def status(self, timeout_in_sec=Timeout.GETTER):
        return self._rpcHandler.receivePickable(
            self._statusSocket,
            timeout_in_sec)[self._axis-1]

    @override
    def snapshot(self,
                 prefix,
                 timeout_in_sec=Timeout.GETTER):
        self._logger.notice("Getting snapshot for %s " % prefix)
        status = self.status(timeout_in_sec=timeout_in_sec)
        return Snapshotable.prepend(prefix, status.as_dict())

    @override
    def home(self,
             timeout_in_sec=Timeout.SETTER):
        self._logger.notice("Homing")
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'home',
            [self._axis],
            timeout=timeout_in_sec)

    @override
    def move_to(self,
                position_in_steps,
                timeout_in_sec=Timeout.SETTER):
        self._logger.notice("Moving to %f" % position_in_steps)
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'move_to',
            [self._axis, position_in_steps],
            timeout=timeout_in_sec)

    @override
    def move_by(self,
                position_in_steps,
                timeout_in_sec=Timeout.SETTER):
        self._logger.notice("Moving by %f" % position_in_steps)
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'move_by',
            [self._axis, position_in_steps],
            timeout=timeout_in_sec)

    @override
    def position(self):
        return int(self.status().position)

    @override
    def set_velocity(self,
                velocity_in_steps_per_second,
                timeout_in_sec=Timeout.SETTER):
        self._logger.notice("Setting velocity to %f" % velocity_in_steps_per_second)
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'set_velocity',
            [self._axis, velocity_in_steps_per_second],
            timeout=timeout_in_sec)

    @override
    def velocity(self):
        return int(self.status().velocity)
