# -*- coding: UTF-8 -*-
from spiders import (
    WholeInvestPro,
    ShanXiJianBangZhiLianCloud,
    ShaanXiElectronicBiddingPro,
    China_BulletinList,
    GanSuWisdomWeb,
    JiLinOnlineBiddingPro,
    AnHuiProvicePlatformPro,
    AnHuiProvinceOnlineInvestPro,
    YuanBoWeb,
    BiaoShiTongBussiness,
    ShangHaiBaoWubiddingBussiness,
    FuJianPublicResourceCenter,
    ChineseProcurementNetworkofYunNan,

    LandPublicOpinion,
    # ChinaNatureService,
    MarvellousVerticalHorizontal,
    AnHuiWholeBidding, DaLianZhongGongProcurementManagenmentPlatform
)

if __name__ == '__main__':

    # dict 调用 爬虫脚本
    switch_go = {

        "全国投资项目在线审批监管平台": WholeInvestPro.WholeInvestPro().run,

        "陕西投资集团华山招标有限公司": ShaanXiElectronicBiddingPro.ShaanXiElectronicBiddingPro().main,

        "山西建邦集团有限公司": ShanXiJianBangZhiLianCloud.ShanXiJianBangZhiLianCloud().queue_run,

        "甘肃智慧阳光采购平台": GanSuWisdomWeb.GanSuWisdomWeb().main,

        "全国投资项目在线审批监管平台-吉林省": JiLinOnlineBiddingPro.JiLinOnlineBidding().parse,

        "安徽省公共资源交易监管网": AnHuiProvicePlatformPro.AnHuiProvincePlatformPro().run,

        "全国投资项目在线审批监管平台-安徽省": AnHuiProvinceOnlineInvestPro.AnHuiProvinceOnlineInvest().main,

        "元博网": YuanBoWeb.YuanBoWeb().parse,

        "标事通": BiaoShiTongBussiness.BiaoShiTongBussiness().get_data,

        "欧贝_宝武资源有限公司": ShangHaiBaoWubiddingBussiness.ShangHaiBaoWubiddingBussiness().main,

        "福建省公共资源交易公共服务平台": FuJianPublicResourceCenter.FuJianPublicResourceCenter().parse,

        "中国政府采购网云南分网": ChineseProcurementNetworkofYunNan.YunNanCaiGouSpider().main,

        # "大唐电商技术有限公司 大唐电子商务平台": DaTang.DaTangSpider().run,

        # "大唐电商技术有限公司 大唐电子商务平台_1": DaTang.DaTangSpider().run_1,

        # "大唐电商技术有限公司 大唐电子商务平台_2": DaTang.DaTangSpider().run_2(),

        "土地舆情网": LandPublicOpinion.LandPublicOpinion().main,

        # 暂时不用更新
        # "自然资源部政务服务门户": ChinaNatureService.ChinaNatureService().run,

        "精彩纵横": MarvellousVerticalHorizontal.Marvellousverticalhorizontal().parse,

        "全国招标信息网-安徽": AnHuiWholeBidding.AnHuiWholeBidding().run,

        "大连重工电子采购平台": DaLianZhongGongProcurementManagenmentPlatform.DaLianZhongGongProcurementManagenmentPlatform().run,

        "中国招标投标公共服务平台_全部": China_BulletinList.ChinaBulletinList().get_data,

    }


    def TimerRun():
        for key in switch_go:
            try:
                switch_go[key]()
            except Exception as e:
                print(e)


    from apscheduler.schedulers.blocking import BlockingScheduler

    TimerRun()
    sched = BlockingScheduler()
    sched.add_job(TimerRun, 'cron', hour=21, minute=30, misfire_grace_time=3600)
    sched.start()
