#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#

import asyncio
import traceback
from asyncio import Task
from typing import List, Dict, Callable, Coroutine

import mesh.log as log
import mesh.tool as tool
from mesh.kinds import Topic, Timeout, Event
from mesh.macro import spi, ServiceLoader, Binding
from mesh.mpc import ServiceProxy
from mesh.prsim import Scheduler, Subscriber


async def period_emitter(duration: int, trigger: Callable[[Topic], Coroutine], topic: Topic):
    while True:
        await trigger(topic)
        await asyncio.sleep(duration / 1000)


@spi("python")
class PythonScheduler(Scheduler):

    def __init__(self):
        self.remote = ServiceProxy.default_proxy(Scheduler)
        self.tasks: Dict[str, Task] = {}

    async def timeout(self, timeout: Timeout, duration: int) -> str:
        return ''

    async def cron(self, cron: str, binding: Topic) -> str:
        return ''

    async def period(self, duration: int, binding: Topic) -> str:
        task_id = tool.next_id()
        log.info(f"Next task {task_id} has been submit.")
        task = asyncio.create_task(period_emitter(duration, self.emit, binding))
        self.tasks[task_id] = task
        return task_id

    async def dump(self) -> List[str]:
        task_ids = []
        for task_id, _ in self.tasks.items():
            task_ids.append(task_id)
        return task_ids

    async def cancel(self, task_id: str) -> bool:
        return await self.stop(task_id)

    async def stop(self, task_id: str) -> bool:
        task = self.tasks.get(task_id, None)
        if task:
            task.cancel()
            self.tasks.__delitem__(task_id)
        return True

    async def emit(self, topic: Topic) -> bool:
        subscribers = ServiceLoader.load(Subscriber).list('')
        for subscriber in subscribers:
            try:
                bindings = Binding.get_binding_if_present(subscriber)
                if not topic.matches(bindings):
                    continue
                await subscriber.subscribe(await Event.new_instance({}, topic))
            except BaseException as e:
                print(traceback.format_exc())
                log.error(f"{e}")

        return True

    async def shutdown(self, duration: int) -> bool:
        for _, task in self.tasks.items():
            task.cancel()
        self.tasks.clear()
        return True
