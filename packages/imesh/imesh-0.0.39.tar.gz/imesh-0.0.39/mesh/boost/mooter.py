#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
import asyncio
import multiprocessing
import os
import signal
from asyncio import CancelledError
from multiprocessing import Process
from threading import Event
from typing import List

import mesh.environ as env
import mesh.log as log
import mesh.tool as tool
from mesh.macro import ServiceLoader
from mesh.mpc import Provider
from mesh.prsim import RuntimeHook


class MooterThread(RuntimeHook):
    def __init__(self):
        self.http1: Provider = ServiceLoader.load(Provider).get("http")
        self.http2: Provider = ServiceLoader.load(Provider).get("grpc")
        self.hooks = ServiceLoader.load(RuntimeHook).list('')
        self.waiter = Event()

    async def start(self):
        for hook in self.hooks:
            await hook.start()
        self.add_exit_hook()
        await self.http1.start(f"0.0.0.0:{tool.get_mesh_runtime().port + 1}", None)
        await self.http2.start(f"0.0.0.0:{tool.get_mesh_runtime().port}", None)

    async def stop(self):
        await self.http1.close()
        await self.http2.close()
        for hook in self.hooks:
            await hook.stop()

    async def refresh(self):
        await self.stop()
        await self.start()

    async def wait(self):
        try:
            await self.http1.wait()
            await self.http2.wait()
            await self.stop()
            # self.waiter.wait()
        except CancelledError as e:
            await self.stop()
            log.info(f"{env.System.environ().get_mesh_name()} has been stop gracefully. ")
        except KeyboardInterrupt:
            await self.stop()
            log.info(f"{env.System.environ().get_mesh_name()} has been stop gracefully. ")

    async def start_wait(self):
        await self.start()
        await self.wait()

    def add_exit_hook(self):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        try:
            asyncio.run(self.stop())
        except KeyboardInterrupt:
            pass
        finally:
            self.waiter.set()


class Mooter(RuntimeHook):

    def __init__(self):
        self.main: RuntimeHook = MooterThread()
        self.workers: List[Process] = []

    @staticmethod
    def start_in_proc(addr: str):
        os.environ.setdefault("MESH_RUNTIME", addr)
        mooter = MooterThread()
        asyncio.run(mooter.start_wait())

    async def start(self):
        await self.main.start()
        self.workers.clear()
        for idx in range(min(tool.get_proc(), multiprocessing.cpu_count() * 2)):
            addr = f"0.0.0.0:{tool.get_mesh_runtime().port - 2 * (idx + 1)}"
            name = f"mesh-worker-{idx}"
            self.workers.append(Process(target=self.start_in_proc, name=name, args=(addr,)))
        for worker in self.workers:
            try:
                worker.start()
            except BaseException as e:
                log.error("", e)

    async def stop(self):
        await self.main.stop()
        for worker in self.workers:
            worker.terminate()
            worker.join()
        log.info("Mesh has been graceful exit.")

    async def refresh(self):
        await self.stop()
        await self.start()

    async def wait(self):
        await self.main.wait()
        await self.stop()
