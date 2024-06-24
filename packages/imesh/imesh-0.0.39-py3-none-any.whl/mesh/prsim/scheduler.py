#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#

from abc import ABC, abstractmethod
from typing import List

from mesh.kinds import Timeout, Topic
from mesh.macro import spi, mpi


@spi("python")
class Scheduler(ABC):

    @abstractmethod
    @mpi("mesh.schedule.timeout")
    async def timeout(self, timeout: Timeout, duration: int) -> str:
        """
        Schedules the specified {@link Timeout} for one-time execution after
        the specified delay.
        :param timeout:
        :param duration:
        :return:
        """
        pass

    @abstractmethod
    @mpi("mesh.schedule.cron")
    async def cron(self, cron: str, binding: Topic) -> str:
        """
        Schedules with the cron expression. "0 * * 1-3 * ? *"
        :param cron:
        :param binding:
        :return:
        """
        pass

    @abstractmethod
    @mpi("mesh.schedule.period")
    async def period(self, duration: int, binding: Topic) -> str:
        """
        Releases all resources acquired by this {@link Scheduler} and cancels all
        tasks which were scheduled but not executed yet.
        :param duration:
        :param binding:
        :return:
        """
        pass

    @abstractmethod
    @mpi("mesh.schedule.dump")
    async def dump(self) -> List[str]:
        """
        Dump all taskIds, only effected in pvm.
        :return:
        """
        pass

    @abstractmethod
    @mpi("mesh.schedule.cancel")
    async def cancel(self, task_id: str) -> bool:
        """
        Cancel the pending tasks.
        :param task_id:
        :return:
        """
        pass

    @abstractmethod
    @mpi("mesh.schedule.stop")
    async def stop(self, task_id: str) -> bool:
        """
        Stop the pending tasks.
        :param task_id:
        :return:
        """
        pass

    @abstractmethod
    @mpi("mesh.schedule.emit")
    async def emit(self, binding: Topic) -> bool:
        """
        Shutdown the scheduler.
        :param binding:
        :return:
        """
        pass

    @abstractmethod
    @mpi("mesh.schedule.shutdown")
    async def shutdown(self, duration: int) -> bool:
        """
        Shutdown the scheduler.
        :param duration:
        :return:
        """
        pass
