# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
factory = clientApi.GetEngineCompFactory()

#获取levelId
levelId = clientApi.GetLevelId()

class solarStormModClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.ListenForEvent("solarStormMod", "solarStormModServerSystem", 'FirePlayerEvent', self, self.OnFirePlayerEvent)
    
    def OnFirePlayerEvent(self,args):

        compCreatePostProcess = factory.CreatePostProcess(levelId)

        isCheckVignetteEnabled = compCreatePostProcess.CheckVignetteEnabled()
        isCheckColorAdjustmentEnabled = compCreatePostProcess.CheckColorAdjustmentEnabled()

        compCreatePostProcess.SetEnableColorAdjustment(True)
        if(args["hasSunglasses"] == False and args["code"] == 0):
            # 调整亮度值为1.1
            compCreatePostProcess.SetColorAdjustmentBrightness(1.1)
            # 调整对比度值为1.5
            compCreatePostProcess.SetColorAdjustmentContrast(1.5)
            if isCheckVignetteEnabled == True:
                compCreatePostProcess.SetEnableVignette(False)

        elif(args["hasSunglasses"] == True and args["code"] == 0):
            if isCheckVignetteEnabled == True:
                compCreatePostProcess.SetEnableVignette(False)
            if isCheckColorAdjustmentEnabled == True:
                compCreatePostProcess.SetEnableColorAdjustment(False)
                # 调整亮度值为1
                compCreatePostProcess.SetColorAdjustmentBrightness(1)
                # 调整对比度值为1
                compCreatePostProcess.SetColorAdjustmentContrast(1)

        elif(args["hasSunglasses"] == False and args["code"] == 1):
            # 调整亮度值为1.5
            compCreatePostProcess.SetColorAdjustmentBrightness(1.5)
            # 调整对比度值为1.5
            compCreatePostProcess.SetColorAdjustmentContrast(1.5)

            if isCheckVignetteEnabled == False:
                compCreatePostProcess.SetEnableVignette(True)

                # 调整渐晕中心位置为屏幕中心
                compCreatePostProcess.SetVignetteCenter((0.5,0.3))

                # 设置颜色值
                compCreatePostProcess.SetVignetteRGB((255,255,55))

                # 调整渐晕半径为0.5
                compCreatePostProcess.SetVignetteRadius(0.6)

                # 调整渐晕模糊系数为0.5
                compCreatePostProcess.SetVignetteSmoothness(0.3)
        elif(args["hasSunglasses"] == True and args["code"] == 2):
            if isCheckVignetteEnabled == True:
                compCreatePostProcess.SetEnableVignette(False)
            if isCheckColorAdjustmentEnabled == True:
                compCreatePostProcess.SetEnableColorAdjustment(False)


    # 监听引擎OnScriptTickClient事件，引擎会执行该tick回调，1秒钟30帧
    def OnTickClient(self):
        """
        Driven by event, One tick way
        """
        pass

    # 被引擎直接执行的父类的重写函数，引擎会执行该Update回调，1秒钟30帧
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):
        pass
