# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 16:56:56 2022

@author: luizf
"""
from connect import *
import win32com.client
ExcelApp = win32com.client.GetActiveObject("Excel.Application")

wb = ExcelApp.Workbooks.Open(r"C:\Users\luizf\Documents\FEMAP\python\dogram\joint.xlsx")

ws = wb.Worksheets("Joint")
cont=4

while ws.Range("K"+str(cont)).Value != None:

    plate1 = ws.Range("K"+str(cont)).Value
    plate1_spl=plate1.split(",")
    plate1_list= list(map(int,plate1_spl))

    plate2 = ws.Range("L"+str(cont)).Value
    plate2_spl=plate2.split(",")
    plate2_list= list(map(int,plate2_spl))

    NX1=plate1_list.copy()
    NX2=plate2_list.copy()
    NXY1=plate1_list.copy()
    NXY2=plate2_list.copy()
    NX1.append("Nx")
    NX2.append("Nx")
    NXY1.append("Nxy")
    NXY2.append("Nxy")
    names=['NX1','NXY1','NX2','NXY2']

    res=(((elres(NX1)+ elres(NX2))*20)**2 + ((elres(NXY1) + elres(NXY2))*20)**2)**0.5
    dfmax=dispMax(res,[NX1,NXY1,NX2,NXY2],names)
    df_array1 = dfmax.to_records()
    df_array2 = df_array1.tolist()
    ws.Range("D"+str(cont)+":J"+str(cont)).Value=df_array2
    cont=cont+1