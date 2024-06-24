# Copyright (c) 2018-2024 by xcube team and contributors
# Permissions are hereby granted under the terms of the MIT License:
# https://opensource.org/licenses/MIT.


from xcube.server.api import Context
from xcube.webapi.common.context import ResourcesContext
from ...datasets.context import DatasetsContext
from ...tiles.context import TilesContext


class WmtsContext(ResourcesContext):
    _feature_index: int = 0

    def __init__(self, server_ctx: Context):
        super().__init__(server_ctx)
        self._tiles_ctx = server_ctx.get_api_ctx("tiles", cls=TilesContext)
        self._datasets_ctx = server_ctx.get_api_ctx("datasets", cls=DatasetsContext)

    @property
    def tiles_ctx(self) -> TilesContext:
        return self._tiles_ctx

    @property
    def datasets_ctx(self) -> DatasetsContext:
        return self._datasets_ctx
