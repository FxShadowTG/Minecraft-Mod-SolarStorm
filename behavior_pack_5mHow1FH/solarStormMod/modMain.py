# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi


@Mod.Binding(name="solarStormMod", version="0.0.1")
class solarStormMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def solarStormModServerInit(self):
        serverApi.RegisterSystem("solarStormMod","solarStormModServerSystem","solarStormMod.solarStormModServerSystem.solarStormModServerSystem")
        print("服务注册成功")

    @Mod.DestroyServer()
    def solarStormModServerDestroy(self):
        print("服务销毁成功")

    @Mod.InitClient()
    def solarStormModClientInit(self):
        clientApi.RegisterSystem("solarStormMod","solarStormModClientSystem","solarStormMod.solarStormModClientSystem.solarStormModClientSystem")
        print("客户注册成功")

    @Mod.DestroyClient()
    def solarStormModClientDestroy(self):
        print("客户销毁成功")
