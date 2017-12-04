from pyecharts import Gauge, Line  # dynamically load the component 
from dbAccess import Connector
from readConfig import DecodeConfig
import json
import random

monitorData = DecodeConfig("db.config")
monitorData.getConfig(option = "hprt9")

class DataRequest(object):

    @property
    def cpu(self):
        charts = {}
        cpudata = {} 
        dataDB = Connector(monitorData.connString)
        dataDB.sqlQuery = """SELECT [MachineName]
                                    ,[CounterValue] = (
                                        select [CounterValue] 
                                        from [dbo].[CounterData] 
                                        where CounterID = main.CounterID 
                                        and [CounterDateTime] = (
						                    select max([CounterDateTime])
                                            from [dbo].[CounterData]
                                            where CounterID = main.CounterID
                                            ) 
						            )
                                FROM [dbo].[CounterDetails] main
                                Where ObjectName = 'Processor'
                            """
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose()
        for i in data:
            key = i[0].replace("\\\\","")
            cpudata[key] = i[1]

        bicwkr3 = Gauge("Bicwkr3")
        bicwkr3.add("", "CPU", round(cpudata["BICWKR3"],2), angle_range=[180, 0], scale_range=[0, 100], is_legend_show=False)
        bicwkr3.options['series'][0]['axisLabel'] = {}
        bicwkr3.options['series'][0]['axisLabel']['show'] = False
        bicwkr4 = Gauge("Bicwkr4")
        bicwkr4.add("", "CPU", round(cpudata["BICWKR4"],2), angle_range=[180, 0], scale_range=[0, 100], is_legend_show=False)
        bicwkr4.options['series'][0]['axisLabel'] = {}
        bicwkr4.options['series'][0]['axisLabel']['show'] = False
        bicwkr5 = Gauge("Bicwkr5")
        bicwkr5.add("", "CPU", round(cpudata["BICWKR5"],2), angle_range=[180, 0], scale_range=[0, 100], is_legend_show=False)
        bicwkr5.options['series'][0]['axisLabel'] = {}
        bicwkr5.options['series'][0]['axisLabel']['show'] = False
        bicwkr6 = Gauge("Bicwkr6")
        bicwkr6.add("", "CPU", round(cpudata["BICWKR6"],2), angle_range=[180, 0], scale_range=[0, 100], is_legend_show=False)
        bicwkr6.options['series'][0]['axisLabel'] = {}
        bicwkr6.options['series'][0]['axisLabel']['show'] = False

        #attr = []
        #v1 = []
        #dataDB.sqlQuery = '''EXEC [dbo].[Processor]
		      #                    @MachineName = N'BICWKR3',
		      #                    @Num = N'1'
        #                  '''
        #dataDB.connOpen()
        #dataRes = dataDB.execQuery()
        #data = dataRes.fetchall()
        #dataDB.connClose()

        attr = ["{}d".format(i) for i in range(30)]
        v1 = [random.randint(1, 100) for _ in range(30)]
        line = Line("CPU usage trend")
        line.add("", attr, v1, is_label_show = True, is_datazoom_show = False)

        wkrchart3 = json.dumps(bicwkr3._option, indent=4, ensure_ascii=False)
        wkrchart4 = json.dumps(bicwkr4._option, indent=4, ensure_ascii=False)
        wkrchart5 = json.dumps(bicwkr5._option, indent=4, ensure_ascii=False)
        wkrchart6 = json.dumps(bicwkr6._option, indent=4, ensure_ascii=False)
        cputrend = json.dumps(line._option, indent=4, ensure_ascii=False)

        charts["bicwkr3"] = wkrchart3
        charts["bicwkr4"] = wkrchart4
        charts["bicwkr5"] = wkrchart5
        charts["bicwkr6"] = wkrchart6
        charts["cputrend"] = cputrend

        f_charts = json.dumps(charts, indent=4, ensure_ascii=False)

        return f_charts
    
    @property
    def memory(self):
        charts = {}
        memorydata = {} 
        dataDB = Connector(monitorData.connString)
        dataDB.sqlQuery = """SELECT [MachineName]
                                   ,[CounterValue] = 
	                                (select [CounterValue] 
                                     from [dbo].[CounterData] 
                                     where CounterID = main.CounterID 
                                     and [CounterDateTime] = (
				                         select max([CounterDateTime])
                                         from [dbo].[CounterData]
                                         where CounterID = main.CounterID
                                         ) 
		                            )/1.0 * 100/
		                            (select Memory 
		                             from [dbo].[Hardware] 
		                             where MachineName = main.MachineName)
                             FROM [dbo].[CounterDetails] main
                             Where ObjectName = 'Memory'
                            """
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose()
        for i in data:
            key = i[0].replace("\\\\","")
            memorydata[key] = i[1]

        bicwkr3 = Gauge("Bicwkr3")
        bicwkr3.add("", "Memory", round(memorydata["BICWKR3"],2), angle_range=[180, 0], scale_range=[0, 100], is_legend_show=False)
        bicwkr3.options['series'][0]['axisLabel'] = {}
        bicwkr3.options['series'][0]['axisLabel']['show'] = False
        bicwkr4 = Gauge("Bicwkr4")
        bicwkr4.add("", "Memory", round(memorydata["BICWKR4"],2), angle_range=[180, 0], scale_range=[0, 100], is_legend_show=False)
        bicwkr4.options['series'][0]['axisLabel'] = {}
        bicwkr4.options['series'][0]['axisLabel']['show'] = False
        bicwkr5 = Gauge("Bicwkr5")
        bicwkr5.add("", "Memory", round(memorydata["BICWKR5"],2), angle_range=[180, 0], scale_range=[0, 100], is_legend_show=False)
        bicwkr5.options['series'][0]['axisLabel'] = {}
        bicwkr5.options['series'][0]['axisLabel']['show'] = False
        bicwkr6 = Gauge("Bicwkr6")
        bicwkr6.add("", "Memory", round(memorydata["BICWKR6"],2), angle_range=[180, 0], scale_range=[0, 100], is_legend_show=False)
        bicwkr6.options['series'][0]['axisLabel'] = {}
        bicwkr6.options['series'][0]['axisLabel']['show'] = False

        attr = ["{}d".format(i) for i in range(30)]
        v1 = [random.randint(1, 100) for _ in range(30)]
        line = Line("Memory usage trend")
        line.add("", attr, v1, is_label_show = True, is_datazoom_show = True)

        wkrchart3 = json.dumps(bicwkr3._option, indent=4, ensure_ascii=False)
        wkrchart4 = json.dumps(bicwkr4._option, indent=4, ensure_ascii=False)
        wkrchart5 = json.dumps(bicwkr5._option, indent=4, ensure_ascii=False)
        wkrchart6 = json.dumps(bicwkr6._option, indent=4, ensure_ascii=False)
        memorytrend = json.dumps(line._option, indent=4, ensure_ascii=False)

        charts["bicwkr3"] = wkrchart3
        charts["bicwkr4"] = wkrchart4
        charts["bicwkr5"] = wkrchart5
        charts["bicwkr6"] = wkrchart6
        charts["memorytrend"] = memorytrend

        f_charts = json.dumps(charts, indent=4, ensure_ascii=False)

        return f_charts

    @property
    def diskSpace(self):
        pass

    @property
    def caseResults(self):
        pass

    @property
    def ritSummary(self):
        pass