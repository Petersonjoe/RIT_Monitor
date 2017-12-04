#-*- coding: utf-8 -*-

DIRECT_QUERY = {
    "cpu" : """SELECT [MachineName]
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
            """,
    "memory": """SELECT [MachineName]
                        ,[CounterValue] = 100 - 
	                    (select [CounterValue] 
                            from [dbo].[CounterData] 
                            where CounterID = main.CounterID 
                            and [CounterDateTime] = (
				                select max([CounterDateTime])
                                from [dbo].[CounterData]
                                where CounterID = main.CounterID
                                ) 
		                )/1.0 * 100/
		                (select Total_Memory 
		                    from [dbo].[HardWare_Parameters] 
		                    where MachineName = main.MachineName)
                    FROM [dbo].[CounterDetails] main
                    Where ObjectName = 'Memory'
                """,
    "disk": """select aa.MachineName,
	                  aa.InstanceName,
                      CounterValue = 100 - (select CounterValue 
	                                          from dbo.CounterData
							                 where CounterID = aa.CounterID
							                   and CounterDateTime = (
								                   select max(CounterDateTime)
									                 from dbo.CounterData
									                where CounterID = aa.CounterID
								               )
							               )
                 from dbo.CounterDetails aa  
                where aa.ObjectName = 'LogicalDisk' 
                order by aa.MachineName, aa.InstanceName
            """,
    "case": """SELECT [Case] = sum([CaseAmount])
                     ,[FailedCase] = sum([FailedCaseAmount])
                     ,[PendingCase] = sum([PendingCaseAmount])
                     ,[ProcessingCase] = sum([ProcessingCaseAmount])
                FROM [dbo].[mainpage_case_realtime_data]
            """,
    "wkrpage_case_summary": """SELECT  [InstanceName]
                                      ,[CaseAmount]
                                      ,[RejectCase]
                                      ,[FailedCaseAmount]
                                      ,[PendingCaseAmount]
                                      ,[ProcessingCaseAmount]
                                      ,[CompletedCase]
                                      ,[ValidationFailedCase]
                                      ,[CancelledCase]
                                      ,[ReadyCase]
                                  FROM [dbo].[wkrpage_case_summary_data]
                                 WHERE [InstanceName] = '{}'
                            """,
    "wkrpage_case_list":"""select  [InstanceName]
                                  ,[ExecCaseID]
                                  ,[packageID]
                                  ,[PackageName]
                                  ,[Owner]
                                  ,[CaseStatus]
                                  ,[CaseCreatedDate]
	                              ,[SizeOfData] = case when isnull([SizeOfData],'') = '' then 0 else [SizeOfData] end
	                              ,[SizeOfLog] = case when isnull([SizeOfLog],'') = '' then 0 else [SizeOfLog] end
                                  ,[SumOfDataRecords] = case when isnull([SumOfDataRecords],'') = '' then 0 else [SumOfDataRecords] end
	                              ,[Runtime]
                                  ,[DataRecordsIn] = sum(case when [taskcategory] like 'fetch%' then [QtyOfTaskData] else 0 end)
	                              ,[DataRecordsOut] = sum(case when [taskcategory] like 'dispatch%' then [QtyOfTaskData] else 0 end)
                              from [dbo].[wkrpage_case_list_data] main
                             where InstanceName = '{}'
                             group by 
                                   [InstanceName]
                                  ,[ExecCaseID]
                                  ,[packageID]
                                  ,[PackageName]
                                  ,[Owner]
                                  ,[CaseStatus]
                                  ,[CaseCreatedDate]
	                              ,[SizeOfData]
	                              ,[SizeOfLog]
                                  ,[SumOfDataRecords]
	                              ,[Runtime]
                            order by [InstanceName], CaseCreatedDate desc
                       """,
    "case_page_sankey":{
                      "case": """SELECT [ExecCaseID]
                                ,[PackageID]
                                ,[TaskID]
                                ,[DataTableID]
                                ,[SourceNode]
                                ,[CaseName]
                                ,[DestNode]
                            FROM [dbo].[casepage_case_source_destination]
                           WHERE ExecCaseID = '{}'
                       """,
                       "pkg": """SELECT [ExecCaseID]
                                        ,[PackageID]
                                        ,[TaskID]
                                        ,[DataTableID]
                                        ,[SourceNode]
                                        ,[CaseName]
                                        ,[DestNode]
                                    FROM [OneBEsPlus_Perfmon_Hist].[dbo].[casepage_case_source_destination]
                                   WHERE [PackageID] = '{}'
                                     AND ExecCaseID = (select top 1 ExecCaseID 
                                                         from dbo.[casepage_case_source_destination]
					                                    where PackageID = '{}')
                       """
                       },
    "case_page_kpi":"""SET NOCOUNT ON;
                       EXEC [dbo].[sp_Casepage_KPIs_response] @caseid = N'{}';
                    """
    } 

TREND_QUERY = {
    "cpu" : """SET NOCOUNT ON; 
               exec [dbo].[sp_Mainpage_Cpu_Trend] @index = 'Processor';
            """,
    "memory": """SET NOCOUNT ON; 
                 exec [dbo].[sp_Mainpage_Cpu_Trend] @index = 'Memory';
              """,
    "disk": """SET NOCOUNT ON; 
                 exec [dbo].[sp_Mainpage_Cpu_Trend] @index = 'LogicalDisk';
            """,
    "casepage_tat":
           {
                "pkg": """SET NOCOUNT ON;
                          exec [dbo].[sp_Casepage_TAT_Response] @packageid = N'{}';
                """,
                "case": """SET NOCOUNT ON;
                           exec [dbo].[sp_Casepage_TAT_Response] @caseid = N'{}';
                """
           }
    }