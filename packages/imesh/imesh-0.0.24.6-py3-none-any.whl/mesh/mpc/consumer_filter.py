#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#

from typing import Any, Dict

import mesh.log as log
import mesh.telemetry as telemetry
from mesh.cause import MeshCode, Codeable, MeshException
from mesh.codec import Codec
from mesh.context import Mesh
from mesh.kinds import MeshFlag
from mesh.macro import spi, ServiceLoader
from mesh.mpc.digest import Digest
from mesh.mpc.filter import Filter, Invoker, Invocation, CONSUMER
from mesh.prsim import Metadata, RunMode


@spi(name="consumer", pattern=CONSUMER, priority=0x80000000)
class ConsumerFilter(Filter):

    def invoke(self, invoker: Invoker, invocation: Invocation) -> Any:
        codec: Codec = ServiceLoader.load(Codec).get(MeshFlag.JSON.get_name())
        attachments: Dict[str, str] = invocation.get_parameters().get_attachments()
        for key, value in Mesh.context().get_attachments().items():
            attachments[key] = value
        attachments[Metadata.MESH_TRACE_ID.key()] = Mesh.context().get_trace_id()
        attachments[Metadata.MESH_SPAN_ID.key()] = Mesh.context().get_span_id()
        attachments[Metadata.MESH_TIMESTAMP.key()] = f"{Mesh.context().get_timestamp()}"
        attachments[Metadata.MESH_RUN_MODE.key()] = f"{Mesh.context().get_run_mode()}"
        attachments[Metadata.MESH_URN.key()] = Mesh.context().get_urn()
        attachments[Metadata.MESH_CONSUMER.key()] = codec.encode_string(Mesh.context().get_consumer())
        attachments[Metadata.MESH_PROVIDER.key()] = codec.encode_string(Mesh.context().get_provider())

        digest = Digest()
        try:
            ret = invoker.run(invocation)
            digest.write("C", MeshCode.SUCCESS.get_code())
            return ret
        except BaseException as e:
            if isinstance(e, Codeable):
                digest.write("C", e.get_code())
            else:
                digest.write("C", MeshCode.SYSTEM_ERROR.get_code())
            if isinstance(e, MeshException):
                log.error(f"{digest.trace_id},{Mesh.context().get_urn()},{e.get_message()}")
            raise e


@spi(name="telemetryConsumer", pattern=CONSUMER, priority=0x3fffffff)
class TelemetryConsumerFilter(Filter):

    def invoke(self, invoker: Invoker, invocation: Invocation) -> Any:
        if not RunMode.TRACE.match(Mesh.context().get_run_mode()):
            return invoker.run(invocation)

        attachments: Dict[str, str] = Mesh.context().get_attachments()
        if not telemetry.if_rebuild_span():
            return invoker.run(invocation)
        with telemetry.build_via_remote(attachments, invocation.get_urn().string()):
            current_span = telemetry.get_current_span()
            current_span.set_attribute('mesh-trace-id', Mesh.context().get_trace_id())
            return invoker.run(invocation)
