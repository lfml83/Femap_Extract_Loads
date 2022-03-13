# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 16:35:49 2022

@author: luizf
"""

import pythoncom
import PyFemap
from PyFemap import constants
import sys
import numpy as np
import pandas as pd
from collections import OrderedDict

try:
    existObj = pythoncom.connect(PyFemap.model.CLSID)
    app = PyFemap.model(existObj)

except:
    sys.exist('Femap not Open')

    
rbo = app.feResults
fsElem = app.feSet
out_sel=app.feSet

vector=np.array([7206,7207,7208,3008,3107,3109,3110,3111,3112,3075,3076,3077,3078,3083,3084,3085,3086])

out_sel.AddAll(28)
#fsElem.AddGroup(8,4)
fsElem.AddAll(8)  
#out_ID=[x for x in range(1,4)]
[rc_out, n_fsElem, fsElem_ID] = fsElem.GetArray()
[rc_out, n_out, out_ID] = out_sel.GetArray()

data_matrix = np.zeros((n_fsElem*len(vector),n_out))
out_ID_array = np.asarray(out_ID) 
fsElem_ID_array = np.asarray(fsElem_ID)

for i in range(n_out):
    cont1=0
    cont2=n_fsElem
    for j in range(len(vector)):
        rbo.AddColumn(out_ID[i], vector[j], False)
        rbo.DataNeeded(8,fsElem.ID)
        rbo.Populate()
        rc_get, vals = rbo.GetRowsByID(fsElem.ID)
        data_matrix[cont1:cont2,i]=vals
        rbo.clear()
        cont1=cont1+n_fsElem
        cont2=cont2+n_fsElem
  


map_elem = np.zeros((len(fsElem_ID),len(vector)))
coluna= range(0,len(data_matrix))
cont=0
for i in range(len(vector)):   
    for j in range(len(fsElem_ID)):

        map_elem[j,i]= coluna[cont]
        cont=cont+1




def AngleNodes(Vert, nod1, nod2):

    results = femap.feMeasureAngleBetweenNodes(Vert, nod1, nod2, 0, 0, 0)
    return results[3]


def elres(elem):

    try:
        if elem[len(elem) - 1] == 'Nx':
            load = 7206
        elif elem[len(elem) - 1] == 'Ny':
            load = 7207
        elif elem[len(elem) - 1] == 'Fx':
            load = 3008
        elif elem[len(elem) - 1] == 'Sx':
            load = 3107
        elif elem[len(elem) - 1] == 'Nxy':
            load = 7208      
        elif elem[len(elem) - 1] == 'MaxCS':
            load = [3109,3111]    
        elif elem[len(elem) - 1] == 'MinCS':
            load = [3110,3112]
        elif elem[len(elem) - 1] == 'MaxBS':
            load = [3075,3076,3077,3078,3083,3084,3085,3086]
        elif elem[len(elem) - 1] == 'MinBS':
            load = [3075,3076,3077,3078,3083,3084,3085,3086]
        elif elem[len(elem) - 1] == 'VM':
            load = [7033,7433]

        len_elem = len(elem) - 1
        set_answer = np.zeros((len_elem, n_out))
        # transformando tupla em array

        for i in range(len_elem):

            element_line = np.where(fsElem_ID_array == elem[i])

            if (element_line[0]==None):

                element_line=0

            if (elem[len(elem) - 1] == 'MaxCS') or (elem[len(elem) - 1] == 'MinCS') or elem[len(elem) - 1] == 'MinBS' or elem[len(elem) - 1] == 'MaxBS' or elem[len(elem) - 1] == 'VM':
                set_answer_CS = np.zeros((len(load),n_out))
                set_answer_MCS = np.zeros((1,n_out))

                for j in range(len(load)):
                    maxCS = []
                    response_col = np.where(vector == load[j])
                    try:

                        line_resposta = map_elem[element_line[0], response_col[0]]
                    #conjunto de resposta Max combined stress
                        set_answer_CS[j,:] =data_matrix[int(line_resposta[0]), :]
                    except:
                    #conjunto de resposta Max combined stress
                        set_answer_CS[j,:] =0

                for k in range(n_out):
                    if (elem[len(elem) - 1] == 'MaxCS') or elem[len(elem) - 1] == 'MaxBS' or elem[len(elem) - 1] == 'VM':
                        set_answer_MCS[0,k] = set_answer_CS[:,k].max()
                    elif (elem[len(elem) - 1] == 'MinCS') or elem[len(elem) - 1] == 'MinBS':
                        set_answer_MCS[0,k] = set_answer_CS[:,k].min()
                set_answer[i, :] = set_answer_MCS
            else:
                response_col = np.where(vector == load)
                try:
                    line_resposta = map_elem[element_line[0], response_col[0]]
                    set_answer[i, :] = data_matrix[int(line_resposta[0]), :]
                except:
                    set_answer[i, :] = 0

        return set_answer

    except:

        print('Load Vector "' + str(elem[len(elem) - 1]) + '" does not exist')

        exit()

def elres_result(set_elements,kind):

    if kind == 'Max':
        data_result=np.where(set_elements==set_elements.max())


        try:
            lc=out_ID_array[int(data_result[1])]
            max_data_result= round(set_elements[data_result][0],2)
            return 'Load Case: '+ str(lc),max_data_result,'index: '+ str(int(data_result[0]+1))
        except:
            max_data_result= 0
            lc=0
            return 'Load Case: '+ str(lc),max_data_result,'index: '+ str(0)



        return 'Load Case: '+ str(lc),max_data_result,'index: '+ str(int(data_result[0]+1))

    if kind == 'Min':
        data_result=np.where(set_elements==set_elements.min())

        try:
            lc=out_ID_array[int(data_result[1])]
            max_data_result= round(set_elements[data_result][0],2)
            return 'Load Case: '+ str(lc),max_data_result,'index: '+ str(int(data_result[0]+1))
        except:
            lc=0
            max_data_result= 0
            return 'Load Case: '+ str(lc),max_data_result,'index: '+ str(0)

def area_mean(vect,kind):

    elem = app.feElem
    nlem=len(vect)

    vec_num = vect[0:(nlem)]

    Nx=vec_num.copy()
    Nx.append('Nx')
    Ny=vec_num.copy()
    Ny.append('Ny')
    Nxy=vec_num.copy()
    Nxy.append('Nxy')

    Nxx=elres(Nx)
    Nyy=elres(Ny)
    Nxy=elres(Nxy)


    Sum_A=0
    Sum_N_AX=np.zeros(n_out,)
    Sum_N_AY=np.zeros(n_out)
    Sum_N_AXY=np.zeros(n_out)
    for i in range(nlem):

        elem.Get(vec_num[i])

        FaceArea = elem.GetFaceArea(1)

        Sum_N_AX = Sum_N_AX + Nxx[i]*FaceArea[1]
        Sum_N_AY = Sum_N_AY + Nyy[i]*FaceArea[1]
        Sum_N_AXY = Sum_N_AXY + Nxy[i]*FaceArea[1]
        Sum_A = Sum_A + FaceArea[1]

        N_meanX = Sum_N_AX/Sum_A
        N_meanY = Sum_N_AY/Sum_A
        N_meanXY = Sum_N_AXY/Sum_A

    resxyMax=N_meanXY.max()
    argxyMax = N_meanXY.argmax()
    resxyMin=N_meanXY.min()
    argxyMin = N_meanXY.argmin()

    if abs(resxyMax) > abs(resxyMin):
        resXY = resxyMax
        argxy = argxyMax

    else:
        resXY = resxyMin
        argxy = argxyMin

    if kind == 'Max':
        resx = N_meanX.max()
        argx = N_meanX.argmax()
        resy = N_meanY.max()
        argy = N_meanY.argmax()

    if kind == 'Min':
        resx = N_meanX.min()
        argx = N_meanX.argmin()
        resy = N_meanY.min()
        argy = N_meanY.argmin()

    mat_ans=np.zeros((1,6))
    mat_ans[0,0]=int(out_ID_array[argx])
    mat_ans[0,1]=resx
    mat_ans[0,2]=int(out_ID_array[argy])
    mat_ans[0,3]=resy
    mat_ans[0,4]=int(out_ID_array[argxy])
    mat_ans[0,5]=resXY

    df=pd.DataFrame(mat_ans,index=['-'],columns=['LCx','Nxx','LCy','Nyy','LCxy','Nxy'])

    return df


def dispAll(resultants,lista,colName,indice):

    n_indice=indice-1
    n_lista=len(lista)
    len_lin=len(lista[0])-1
    col_df=[]
    matrix_df=np.zeros((n_out,n_lista))
    for i in range(n_lista):
        #col_df = col_df + [lista[i][len_lin]]

        elres_ans=elres([lista[i][n_indice],lista[i][len_lin]])
        matrix_df[:,i]=elres_ans
    df=pd.DataFrame(matrix_df,index=out_ID_array,columns=colName)
    df['resultant'] = resultants[n_indice,:]
    return df


def dispMax(resultants,lista,colName):

    result_max =elres_result(resultants,'Max')
    indice =int(result_max[2].split(':')[1])
    n_indice=indice-1
    n_lista=len(lista)
    len_lin=len(lista[0])-1
    col_df=[]
    elements=[]
    matrix_df=np.zeros((n_out,n_lista))
    for i in range(n_lista):

        try:
            elements= elements + [lista[i][n_indice]]
            elres_ans=elres([lista[i][n_indice],lista[i][len_lin]])
            matrix_df[:,i]=elres_ans


        except:
            elements= [0]
            matrix_df[:,i]=0


    df=pd.DataFrame(matrix_df,index=out_ID_array,columns=colName)
    df['Result index: ' +str(indice)] = resultants[n_indice,:]
    dfMax=df[df['Result index: ' +str(indice)]==df['Result index: ' +str(indice)].max()]
    #numero de elementos
    final_elements = list(OrderedDict.fromkeys(elements))

    df_col_len = len(colName)

    dfMax.insert(df_col_len, 'Elements', str(final_elements), allow_duplicates=True)

    return dfMax


def dispMin(resultants,lista,colName):

    result_max =elres_result(resultants,'Min')
    indice =int(result_max[2].split(':')[1])
    n_indice=indice-1
    n_lista=len(lista)
    len_lin=len(lista[0])-1
    col_df=[]
    elements=[]
    matrix_df=np.zeros((n_out,n_lista))
    for i in range(n_lista):


        try:
            elements= elements + [lista[i][n_indice]]
            elres_ans=elres([lista[i][n_indice],lista[i][len_lin]])
            matrix_df[:,i]=elres_ans


        except:
            elements= [0]
            matrix_df[:,i]=0

    df=pd.DataFrame(matrix_df,index=out_ID_array,columns=colName)


    df['Result index: ' +str(indice)] = resultants[n_indice,:]
    dfMin=df[df['Result index: ' +str(indice)]==df['Result index: ' +str(indice)].min()]

    final_elements = list(OrderedDict.fromkeys(elements))
    df_col_len = len(colName)
    dfMin.insert(df_col_len, 'Elements', str(final_elements), allow_duplicates=False)

    return dfMin
