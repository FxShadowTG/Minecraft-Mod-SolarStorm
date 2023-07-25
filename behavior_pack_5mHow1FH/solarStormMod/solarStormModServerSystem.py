# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from math import floor
import random
ServerSystem = serverApi.GetServerSystemCls()
factory = serverApi.GetEngineCompFactory()

#获取levelId
levelId = serverApi.GetLevelId()
playerIdList = []
            
class solarStormModServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenEvent()
        self.isTimer = False
        self.updateCD = 0
        print("加载监听ing")
        print("加载监听ok")

    def ListenEvent(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'AddServerPlayerEvent', self, self.OnAddServerPlayerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerRespawnFinishServerEvent', self, self.OnPlayerRespawnFinishServerEvent)

    def OnAddServerPlayerEvent(self,args):
        playerIdList.append(args["id"])

        if self.isTimer == False:
            generator = serverApi.StartCoroutine(firePlayerFunc(self))
            self.isTimer = True

    def OnPlayerRespawnFinishServerEvent(self,args):
        playerId = args["playerId"]
        compCreateEffect = factory.CreateEffect(playerId)
        compCreateEffect.AddEffectToEntity("fire_resistance", 10, 5, False)

    def Update(self):
        if self.updateCD > 15:
            firePlayerFunc(self)
            self.updateCD = 0
        self.updateCD = self.updateCD + 1

    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'AddServerPlayerEvent', self, self.OnAddServerPlayerEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'LoadServerAddonScriptsAfter', self, self.OnLoadServerAddonScriptsAfter)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerRespawnFinishServerEvent', self, self.OnPlayerRespawnFinishServerEvent)
    
    def Destroy(self):
        self.UnListenEvent()

def firePlayerFunc(self):
    # print("firePlayerFunc...")

    compCreateDimension = factory.CreateDimension(levelId)
    # 从游戏开始经过的总帧数
    passedTime = compCreateDimension.GetLocalTime(0)
    # 当前游戏天内的帧数
    timeOfDay = passedTime % 24000
    # print(timeOfDay)
    compCreateGameByLevelId = factory.CreateGame(levelId)

    for playerId in playerIdList:
        #0-12000太阳升起，12001-24000消失
        if timeOfDay > 12000 and timeOfDay < 24000:
            if timeOfDay > 12001 and timeOfDay < 12010:
                compCreateGameByLevelId.SetNotifyMsg("太阳下山了...", serverApi.GenerateColor('BLUE'))
                #清除太阳特效bug
                contentDict = {
                    "code": 0,
                    "hasSunglasses": True
                }
                self.NotifyToClient(playerId,"FirePlayerEvent", contentDict)
            return
        elif timeOfDay > 0 and timeOfDay <= 12000:
            if timeOfDay > 1 and timeOfDay < 10:
                compCreateGameByLevelId.SetNotifyMsg("太阳风暴爆发了...", serverApi.GenerateColor('RED'))

        compCreateGameByPlayerId = factory.CreateGame(playerId)
        entityIdList = compCreateGameByPlayerId.GetEntitiesAround(playerId, 100, None)

        for entityId in entityIdList:

            compCreatePos = factory.CreatePos(entityId)
            entityPos = compCreatePos.GetPos()
            entityPosX = int(floor(entityPos[0]))
            entityPosZ = int(floor(entityPos[2]))

            comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
            dimension = comp.GetEntityDimensionId()

            compCreateBlockInfo = factory.CreateBlockInfo(levelId)
            height = compCreateBlockInfo.GetTopBlockHeight((entityPosX, entityPosZ), dimension)

            contentDict = {
                "code": 0,
                "hasSunglasses": False
            }
            
            # 判断是否为玩家
            compCreateEngineType = factory.CreateEngineType(entityId)
            entityType = compCreateEngineType.GetEngineType()

            # 判断是否为下雨
            compCreateWeather = factory.CreateWeather(levelId)
            isRaining = compCreateWeather.IsRaining()

            # 是的话就通知客户端
            if entityType == 319 and isRaining == False:
                #判断玩家是否带墨镜，是的话携带带墨镜参数
                compCreateItem = factory.CreateItem(entityId)
                itemDict = compCreateItem.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, 0)
                if itemDict != None and itemDict['newItemName'] == "kojyr:item_sunglasses":
                    contentDict["hasSunglasses"] = True

            if(entityPos[1] > height):
                compCreateAttr = factory.CreateAttr(entityId)
                compCreateAttr.SetEntityOnFire(1, 2)

                if isRaining != True:
                    rangeEvent = random.randrange(1,15)
                    compCreateCommand = factory.CreateCommand(levelId)
                    if rangeEvent == 1:
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 air 0 replace water",entityId)
                    elif rangeEvent == 2:
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 dirt 0 replace grass",entityId)
                    elif rangeEvent == 3:
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 dirt_with_roots 0 replace mycelium",entityId)
                    elif rangeEvent == 4:
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 flowing_water 0 replace snow",entityId)
                    elif rangeEvent == 5:    
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 flowing_water 0 replace ice",entityId)
                    elif rangeEvent == 6:
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 flowing_water 0 replace blue_ice",entityId)
                    elif rangeEvent == 7:
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 flowing_water 0 replace frosted_ice",entityId)
                    elif rangeEvent == 8:
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 flowing_water 0 replace packed_ice",entityId)
                    elif rangeEvent == 9:    
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 flowing_water 0 replace snow_layer",entityId)
                    elif rangeEvent == 10:  
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 flowing_water 0 replace powder_snow",entityId)
                    elif rangeEvent == 11:  
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 air 0 replace flowing_water",entityId)
                    elif rangeEvent == 12:  
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 air 0 replace double_plant",entityId)
                    elif rangeEvent == 13:  
                        compCreateCommand.SetCommand("/execute @s ~~~ fill ~-4~-4~-4 ~4~4~4 deadbush 0 replace tallgrass",entityId)
                    elif rangeEvent == 14:  
                        compCreateCommand.SetCommand("/execute @e[type=!player,c=-1,r=200] ~~~ setblock ~~~ fire",entityId)
                    contentDict["code"] = 1
            self.NotifyToClient(entityId,"FirePlayerEvent", contentDict)



