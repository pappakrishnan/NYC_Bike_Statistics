# -*- coding: utf-8 -*-
"""
@author: Venkatesh
"""
import sys
import pandas as pd
import numpy as np
import time

inp=pd.read_csv("E:\data.csv")

inp.starttime=inp.starttime.apply(lambda x: time.mktime(time.strptime(x,"%Y-%m-%d %H:%M:%S")))
inp.stoptime=inp.stoptime.apply(lambda x: time.mktime(time.strptime(x,"%Y-%m-%d %H:%M:%S")))    
inp['difference']=inp['stoptime']-inp['starttime']

#To find mean travel time in seconds
mean_travel= inp["difference"].mean(axis=1)

inp_sorted=inp.sort('starttime')
inp_group=inp_sorted.groupby('bikeid') #group data set based on bikeid

"""for bikeid, group in inp_group:
    print(bikeid)
    print(group)"""

flag=0; unused_time=0;h=0
bikes_hour=np.zeros((24,2))

for bikeid, group in inp_group:
    grp_temp=inp_group.get_group(bikeid).loc[:,('start station id','end station id','starttime','stoptime')]
    grp_temp.index=range(len(grp_temp))
    h+=1; print(bikeid, h)
    
    for f in range(0, len(grp_temp)-1):
        unused_time+=grp_temp.ix[f+1,2]-grp_temp.ix[f,3]
        
        if grp_temp.ix[f,1]!=grp_temp.ix[f+1,0]:
            flag+=1  #missing row
 
        if grp_temp.ix[f,1] in ("8f0f64", "4a4b61") and grp_temp.ix[f+1,0]==grp_temp.ix[f,1]:        
            t1=1383116400.0;t2=t1+3600 
            
            for g in range(24):
                if grp_temp.ix[f,3]<=t2 and grp_temp.ix[f+1,2]>t1:
                    if grp_temp.ix[f,1]=="8f0f64":
                        col=0
                    else:
                        col=1
                    bikes_hour[g][col]+=1
                t1=t2; t2+=3600       
                

Avg_unused_time=unused_time/(len(inp)-len(inp_group))
fraction_missing_rows=flag/(len(inp)+flag)
       
print("Minimum fraction of missing rows:",fraction_missing_rows,"%")
print("Average time spend by a bike at station:", Avg_unused_time)

bikes_hour_station=pd.DataFrame(bikes_hour, index=range(24), columns=['8f0f64','4a4b61'])
print("No. of. bikes at stations 8f0f64 and 4a4b61 every hour on 2013/10/30:")
print(bikes_hour_station.to_csv(sys.stdout))


bikes_hour_arrival=np.zeros((24,5))
inp_group_station=inp_sorted.groupby('end station id')

for Endstation, group in inp_group_station:
    if Endstation in ('912d97','2da8d7','010d01','36ba2f','fa4911'):
        print(Endstation)
        grp_temp_station=inp_group_station.get_group(Endstation).loc[:,('bikeid','stoptime')]
        grp_temp_station.index=range(len(grp_temp_station))
        for ff in range(0, len(grp_temp_station)):
            s1=1385452800; s2=s1+3600
            
            for gg in range(24):
                if grp_temp_station.ix[ff,1]<=s2 and grp_temp_station.ix[ff,1]>s1:
                    if Endstation=="912d97":
                        col=0
                    elif Endstation=="2da8d7":
                        col=1
                    elif Endstation=="010d01":
                        col=2
                    elif Endstation=="36ba2f":
                        col=3
                    else:
                        col=4
                    bikes_hour_arrival[gg][col]+=1
                s1=s2; s2+=3600 


bikes_hour_station_arrival=pd.DataFrame(bikes_hour_arrival, index=range(24), columns=['912d97','2da8d7','010d01','36ba2f','fa4911'])
print("No. of. bikes arriving at stations every hour on 2013/11/26:")
print(bikes_hour_station_arrival.to_csv(sys.stdout)) 
