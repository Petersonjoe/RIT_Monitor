#-*- coding: utf-8 -*-
from dbAccess import Connector
from readConfig import DecodeConfig
from querySettings import DIRECT_QUERY, TREND_QUERY
import json
import random
import time

monitorData = DecodeConfig("db.config")
monitorData.getConfig(option = "hprt9")

monitorHistData = DecodeConfig("db.config")
monitorHistData.getConfig(option = "hprt9_hist")

def _isNone(num):
    if not num:
        return 0.0
    else:
        return num

def _dKey(l):
    d = {}
    if l is not None:
        for i in l:
            if d.has_key(i) and d[i] is not None:
                d[i]  = d[i] + 1
            elif i is not None:
                d[i] = 1
        key = [i for i in d.keys() if d[i] > 1]
        return key
    else:
        return None

class DataRequest(object):

    @property
    def cpu(self):
        charts = {
            "cpudata":{},
            "cputrend":{
                "xdata":[],
                "ydata":{}
                }
            }

        cpudata = {} 
        dataDB = Connector(monitorData.connString)
        dataDB.sqlQuery = DIRECT_QUERY["cpu"]
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose()
        for i in data:
            key = i[0].replace("\\\\","")
            cpudata[key] = round(i[1],2)
        charts["cpudata"] = cpudata

        dataDB.sqlQuery = TREND_QUERY["cpu"]
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose()

        lineRes = {}
        attrRes = {}
        try:
            for row in data:
                if lineRes.has_key(row[0]):
                    lineRes[row[0]].append(round(_isNone(row[2]),2))
                    attrRes[row[0]].append(row[1][0:19])  # resolution into seconds only
                else:
                    lineRes[row[0]] = []
                    lineRes[row[0]].append(round(_isNone(row[2]),2))
                    attrRes[row[0]] = []
                    attrRes[row[0]].append(row[1][0:19])
        except Exception, e:
            print e.message
            return '505'

        attr = ["{}".format(i) for i in attrRes["BICWKR3"]]
        charts["cputrend"]["xdata"] = attr
        charts["cputrend"]["ydata"] = lineRes

        f_charts = json.dumps(charts, indent=4, ensure_ascii=False)

        return f_charts
    
    @property
    def memory(self):
        charts = {
            "memorydata":{},
            "memorytrend":{
                "xdata":[],
                "ydata":{}
                }
            }

        memorydata = {} 
        dataDB = Connector(monitorData.connString)
        dataDB.sqlQuery = DIRECT_QUERY["memory"]
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose()
        for i in data:
            key = i[0].replace("\\\\","")
            memorydata[key] = round(i[1],2)
        charts["memorydata"] = memorydata

        dataDB.sqlQuery = TREND_QUERY["memory"]
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose()

        lineRes = {}
        attrRes = {}
        for row in data:
            if lineRes.has_key(row[0]):
                lineRes[row[0]].append(round(_isNone(row[2]),2))
                attrRes[row[0]].append(row[1][0:19])  # resolution into seconds only
            else:
                lineRes[row[0]] = []
                lineRes[row[0]].append(round(_isNone(row[2]),2))
                attrRes[row[0]] = []
                attrRes[row[0]].append(row[1][0:19])

        attr = ["{}".format(i) for i in attrRes["BICWKR3"]]
        charts["memorytrend"]["xdata"] = attr
        charts["memorytrend"]["ydata"] = lineRes

        f_charts = json.dumps(charts, indent=4, ensure_ascii=False)

        return f_charts

    @property
    def caseResults(self): 
        dataDB = Connector(monitorHistData.connString)
        dataDB.sqlQuery = DIRECT_QUERY["case"]
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()[0]
        dataDB.connClose()
        v1 = list(data)[::-1]  ## data order - [#processingcase, #pendingcase, #failedcase, #case]

        return json.dumps(v1,indent=4,ensure_ascii=False)

    @property
    def diskSpace(self):
        charts = {}
        diskdata = {}

        v1 = [0 for i in range(4)]  ## data order - [bicwkr6, bicwkr5, bicwkr4, bicwkr3]
        v2 = [0 for i in range(4)]  ## data order - v2 sysdrive; v1 dbdrive
        dataDB = Connector(monitorData.connString)
        dataDB.sqlQuery = DIRECT_QUERY["disk"]
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose()
        for arr in data:
            dKey = arr[0].replace('\\\\','').upper()
            if diskdata.has_key(dKey):
                diskdata[dKey][arr[1].replace(':','')] = round(arr[2],2)
            else:
                diskdata[dKey] = {}
                diskdata[dKey][arr[1].replace(':','')] = round(arr[2],2)

        ## process trend data 
        v_data = {}
        attrRes = {}

        dataDB.sqlQuery = TREND_QUERY["disk"]
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose()
        for row in data:
            if v_data.has_key(row[0]):
                if v_data[row[0]].has_key(row[2].replace(':','')):
                    v_data[row[0]][row[2].replace(':','')].append(round(_isNone(row[3]),2))
                    attrRes[row[0]][row[2].replace(':','')].append(row[1])
                else:
                    v_data[row[0]][row[2].replace(':','')] = []
                    v_data[row[0]][row[2].replace(':','')].append(round(_isNone(row[3]),2))
                    
                    attrRes[row[0]][row[2].replace(':','')] = []
                    attrRes[row[0]][row[2].replace(':','')].append(row[1])
            else:
                v_data[row[0]] = {}
                v_data[row[0]][row[2].replace(':','')] = []
                v_data[row[0]][row[2].replace(':','')].append(round(_isNone(row[3]),2))

                attrRes[row[0]] = {}    
                attrRes[row[0]][row[2].replace(':','')] = []
                attrRes[row[0]][row[2].replace(':','')].append(row[1])
         
        charts["xAxisData"] = ['{}'.format(i) for i in attrRes["BICWKR3"]["C"]]
        charts["seriesData"] = v_data
        charts["diskdata"] = diskdata

        f_charts = json.dumps(charts, indent=4, ensure_ascii = False)
        return f_charts

    @staticmethod
    def wkrCaseList(wkrname):
        caselistdata = {
            "wkrname": [],
            "cid": [],
            "pid": [],
            "pname": [],
            "owner": [],
            "cstatus": [],
            "casecreatedate": [],
            "casesize": [],
            "timeconsumed": [],
            "#Records": [],
            "#flowin": [],
            "#flowout": []
            }

        dataDB = Connector(monitorHistData.connString)
        dataDB.sqlQuery = DIRECT_QUERY["wkrpage_case_list"].format(wkrname)
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose
        for row in data:
            caselistdata["wkrname"].append(row[0])
            caselistdata["cid"].append(row[1])
            caselistdata["pid"].append(row[2])
            caselistdata["pname"].append(row[3])
            caselistdata["owner"].append(row[4])
            caselistdata["cstatus"].append(row[5])
            caselistdata["casecreatedate"].append(row[6])
            caselistdata["casesize"].append(row[7] + row[8])
            caselistdata["#Records"].append(row[9])
            caselistdata["timeconsumed"].append(row[10])
            caselistdata["#flowin"].append(row[11])
            caselistdata["#flowout"].append(row[12])

        return caselistdata

    @staticmethod
    def wkrCaseSummary(wkrname):
        summaryData = {
            'RejectCase': -1,
            'ReadyCase': -1,
            'PendingCase': -1,
            'FailedCase': -1,
            'ValidationFailedCase': -1,
            'CancelledCase': -1,
            'ProcessingCase': -1,
            'CompletedCase': -1
            }

        dataDB = Connector(monitorHistData.connString)
        dataDB.sqlQuery = DIRECT_QUERY["wkrpage_case_summary"].format(wkrname)
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose
        summaryData["RejectCase"] = data[0][2]
        summaryData["ReadyCase"] = data[0][9]
        summaryData["PendingCase"] = data[0][4]
        summaryData["FailedCase"] = data[0][3]
        summaryData["ValidationFailedCase"] = data[0][7]
        summaryData["CancelledCase"] = data[0][8]
        summaryData["ProcessingCase"] = data[0][5]
        summaryData["CompletedCase"] = data[0][6]

        return json.dumps(summaryData, indent=4, ensure_ascii = False)

    @staticmethod
    def casePageSankey(index, **kwargs):
        dataSet = {
            "cid": [],
            "pid": [],
            "tid": [],
            "dtid": [],
            "source": [],
            "cname": [],
            "dest": []
            }
        f_data = {
            "nodes": [],
            "links": [],
            "pid": []
            }

        dataDB = Connector(monitorHistData.connString)
        if(kwargs["isCase"]):
            dataDB.sqlQuery = DIRECT_QUERY["case_page_sankey"]["case"].format(index)
        else:
            dataDB.sqlQuery = DIRECT_QUERY["case_page_sankey"]["pkg"].format(index, index)
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose
        for row in data:
            dataSet["cid"].append(row[0])
            dataSet["pid"].append(row[1])
            dataSet["tid"].append(row[2])
            dataSet["dtid"].append(row[3])
            dataSet["source"].append(row[4])
            dataSet["cname"].append(row[5])
            dataSet["dest"].append(row[6])
        
        f_data["nodes"].append({"name": dataSet["cname"][0]})
        casename = dataSet["cname"][0]
        pkgid = dataSet["pid"][0]

        # for process node
        s_nodes = list(set(dataSet["source"]))
        d_nodes = list(set(dataSet["dest"]))
        conNodes = s_nodes + d_nodes
        conNodes.append(casename)
        dNodes = _dKey(conNodes)

        # generate values
        s_values = {}
        d_values = {}
        s_flag = {}
        d_flag = {}
        for node in s_nodes:
            if (node is not None):
                s_values[node] = len([i for i in range(len(dataSet["source"])) if cmp(dataSet["source"][i],node) == 0])
                s_flag[node] = 0
        for node in d_nodes:
            if (node is not None):
                d_values[node] = len([i for i in range(len(dataSet["dest"])) if cmp(dataSet["dest"][i],node) == 0])
                d_flag[node] = 0

        for i in range(len(dataSet["source"])):
            if (dataSet["source"][i] is not None):
                if (s_flag[dataSet["source"][i]] == 0):
                    if (dataSet["source"][i] in dNodes):
                        node = {"name": dataSet["source"][i] + "_in"}
                        link = {"source": dataSet["source"][i] + "_in", "target": dataSet["cname"][0], "value": s_values[dataSet["source"][i]]}
                    else:
                        node = {"name": dataSet["source"][i]}
                        link = {"source": dataSet["source"][i], "target": dataSet["cname"][0], "value": s_values[dataSet["source"][i]]}
                    f_data["nodes"].append(node)
                    f_data["links"].append(link)
                    s_flag[dataSet["source"][i]] = 1
            if (dataSet["dest"][i] is not None):
                if (d_flag[dataSet["dest"][i]] == 0):
                    if dataSet["dest"][i] in dNodes:
                        node = {"name": dataSet["dest"][i] + "_out"}
                        link = {"source": dataSet["cname"][0], "target": dataSet["dest"][i] + "_out", "value": d_values[dataSet["dest"][i]]}
                    else:
                        node = {"name": dataSet["dest"][i]}
                        link = {"source": dataSet["cname"][0], "target": dataSet["dest"][i], "value": d_values[dataSet["dest"][i]]}
                    f_data["nodes"].append(node)
                    f_data["links"].append(link)
                    d_flag[dataSet["dest"][i]] = 1

        ## need more decoration for extracting data from pid
        f_data["pid"] = pkgid
        response = json.dumps(f_data, indent = 4, ensure_ascii = False)

        if kwargs.has_key("requestType"):
            if cmp(kwargs["requestType"], "web") == 0:
                return casename
            elif cmp(kwargs["requestType"], "ajax") == 0:
                return response    
        else:
            return None

    @staticmethod
    def casePageTAT(index, isCase = 1):
        """
           index: caseid or pkgid
           isCase: whether the caseid provided, 1 yes, 0 no
        """
        TATres = {
            "tasklist": [],
            "timelist": [],
            "tatdata": {},
            "faildata": {}  ## great extensible feature for different matrices
            }

        dataDB = Connector(monitorHistData.connString)
        if isCase:
            dataDB.sqlQuery = TREND_QUERY["casepage_tat"]["case"].format(index)
        else:
            dataDB.sqlQuery = TREND_QUERY["casepage_tat"]["pkg"].format(index)
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose
        
        tmp_tasklist = []
        tmp_timelist = []
        tmp_caseflag = {}
        for row in data:
            tmp_tasklist.append(row[3])
            if not tmp_caseflag.has_key(row[1]):
                tmp_timelist.append(row[2])
                tmp_caseflag[row[1]] = 1

        TATres["tasklist"] = list(set(tmp_tasklist))
        ##if isCase:  ## optimization should aim to differentiate case and pacakge
        for item in TATres["tasklist"]:
            TATres["tatdata"][item] = [0.0 for i in range(len(tmp_timelist))]
            TATres["faildata"][item] = [0.0 for i in range(len(tmp_timelist))]

        # drawback is that cannot deal with duplicated casestart time
        for row in data:
            TATres["tatdata"][row[3]][tmp_timelist.index(row[2])] = float(row[5])
            TATres["faildata"][row[3]][tmp_timelist.index(row[2])] = int(row[7])

        #need ways to filter out the cases created at the same time
        TATres["timelist"] = ['{}'.format(i.strftime('%Y-%m-%d %H:%M')) for i in tmp_timelist]

        result = json.dumps(TATres, indent = 4, ensure_ascii = False)

        return result

    @staticmethod
    def casePageKPI(cid):
        KPIres = {
            "Csize": '',
            "TskMaxVols": '',
            "FailedTskNum": '',
            "TblNum": ''
            }
        dataDB = Connector(monitorHistData.connString)
        dataDB.sqlQuery = DIRECT_QUERY["case_page_kpi"].format(cid)
        dataDB.connOpen()
        dataRes = dataDB.execQuery()
        data = dataRes.fetchall()
        dataDB.connClose

        KPIres["Csize"] = data[0][0] + "Gb"
        KPIres["TskMaxVols"] = data[0][1]
        KPIres["FailedTskNum"] = data[0][2]
        KPIres["TblNum"] = data[0][3]
        
        result = json.dumps(KPIres, indent = 4, ensure_ascii = False)
        return result

        