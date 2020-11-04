# writen by Gesang Yangji, Oct 2020
"""
this file contains the functions that are used to 
1) load the original data from csv files, 
2) extract the target variables for a city in a given year under a emission scenario,
3) match the geoinfo of cities with selected variables,
4) creat a new dataframe for the variable(city, decade) under given scenario

"""
import matplotlib                   
import matplotlib.pyplot as plt     
import numpy as np                  
import pandas as pd 
import os
import csv

#load original csv data and add into a dict
def csv2dict(cityl,yr,scen): 
    filename = os.path.join(cityl,scen,'statistics/ASHRAE.final.'+yr+'.csv')
    mydict = {}
    with open(filename) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            k = row[0]
            v = row[1:]
            mydict.update({k:v})
    return mydict
    
# pull out your target variables and save into a dict with keys are cities
def gettargetvars(CityLname,tar_yr,tar_var,tar_scen):
    vardict = {}
    cities = CityLname
    var = tar_var
    yr = tar_yr
    rcp = tar_scen
    
    for icity in cities:
        data = csv2dict(icity,yr,rcp)
        for i in range(len(data)):
            if list(data.keys())[i] == var:
                k = icity
                v = list(data.values())[i]
                vardict.update({k:v})      
    return vardict
    
# make a new df with latlon and target variables
def creatnewdf(CityLname,tar_yr,tar_var,tar_scen):
    allcities = CityLname
    variable = tar_var
    year = tar_yr
    rcp = tar_scen

    file = 'CityInfo.xlsx'
    fgeo = pd.read_excel(file)
    citynam = []
    lat = []
    lon = []
    var = []
    subsetdata = gettargetvars(allcities,year,variable,rcp)
    for icity,city in enumerate(list(fgeo.City)):
            if city in list(subsetdata.keys()):
                citynam.append(city)
                lat.append(list(fgeo.Lat)[icity])
                lon.append(list(fgeo.Lon)[icity])
                var.append(list(subsetdata[city]))
    data = {'city':citynam,'lat':lat,'lon':lon,year:var}  
    return pd.DataFrame(data)
    
# get target variables for all decades
def getvarsfordecades(CityLname,yrstr,tart_var,scen):
    cityl = CityLname
    years = yrstr
    variable = tart_var
    rcp = scen
    mydf = creatnewdf(cityl,years[0],variable,rcp)
    
    yrlist = years[1:]
    for iy, year in enumerate(yrlist):
        mydf[year] = creatnewdf(CityLname,yrlist[iy],variable,rcp)[year]
    return mydf 
