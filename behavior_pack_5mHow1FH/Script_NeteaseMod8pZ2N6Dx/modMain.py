# -*- coding: utf-8 -*-

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseMod8pZ2N6Dx", version="0.0.1")
class Script_NeteaseMod8pZ2N6Dx(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseMod8pZ2N6DxServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseMod8pZ2N6DxServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseMod8pZ2N6DxClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseMod8pZ2N6DxClientDestroy(self):
        pass
