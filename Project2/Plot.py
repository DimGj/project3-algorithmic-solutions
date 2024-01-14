import sys
import os
import numpy as np
import matplotlib.pyplot as plt


####################################################################
#To run this input 2 files with -l for latent and -d for normal file
####################################################################



def ReadLatentFiles(file_path):
    PointIDs,distanceApprox,distanceLatentBrute,distanceTrue,tApprox,tLatentTrue,tTrue,aF = [],[],[],[],[],[],[],[]

    with open(file_path,'r') as file :
        for line in file:
            parts = line.strip().split(": ")
            if len(parts) == 1:
                continue
            key,value = parts[0],parts[1]
            if key == 'Query':
                PointIDs.append(value)
            elif key == 'distanceApproximate':
                distanceApprox.append(value)
            elif key == 'distanceLatentTrue':
                distanceLatentBrute.append(value)
            elif key == 'distanceTrue':
                distanceTrue.append(value)
            elif key == 'tAverageApproximate':
                tApprox.append(value.split("ms")[0])
            elif key == 'tAverageLatentTrue':
                tLatentTrue.append(value.split("ms")[0])
            elif key == 'tAverageTrue':
                tTrue.append(value.split("ms")[0])
            elif key == 'AF':
                aF.append(value)
    return PointIDs,distanceApprox,distanceLatentBrute,distanceTrue,tApprox,tLatentTrue,tTrue,aF

def ReadFiles(file_path):
    PointIDs,distanceApprox,distanceBrute,tApprox,tTrue,aF = [],[],[],[],[],[]

    with open(file_path,'r') as file :
        for line in file:
            parts = line.strip().split(": ")
            if len(parts) == 1:
                continue
            key,value = parts[0],parts[1]
            if key == 'Query':
                PointIDs.append(value)
            elif key == 'distanceApproximate':
                distanceApprox.append(value)
            elif key == 'distanceTrue':
                distanceBrute.append(value)
            elif key == 'tAverageApproximate':
                tApprox.append(value.split("ms")[0])
            elif key == 'tAverageTrue':
                tTrue.append(value.split("ms")[0])
            elif key == 'AF':
                aF.append(value)

    return PointIDs,distanceApprox,distanceBrute,tApprox,tTrue,aF

def Plot(latent_file,normal_file,isLatent = False):
    PointIDs,distanceApprox,distanceLatentBrute,distanceTrue,tApprox,tLatentTrue,tTrue,aF_latent = ReadLatentFiles(latent_file)
    aF_Latent = list(map(float, aF_latent))

    if isLatent:

        distanceApprox = list(map(float, distanceApprox))
        distanceTrue = list(map(float, distanceTrue))
        distanceLatentBrute = list(map(float, distanceLatentBrute))

        tApprox = list(map(float, tApprox))
        tTrue = list(map(float, tTrue))
        tLatentTrue = list(map(float,tLatentTrue))

            #Create Distances Plot
        CreatePlot(distanceApprox,distanceTrue,PointIDs,title='Scatter Plot for distances',x_label='Query IDs',y_label='Distances',
                   scatter_labels=['Latent Distances','True Distances'],output_file='latent-true_distances')
            #Create Time float
        CreatePlot(tApprox ,tTrue,PointIDs,title='Scatter Plot for time',x_label='Query IDs',y_label='Time (ms)',
                   scatter_labels=['Latent time','True time'],output_file='latent-true_time')
       
        output_file_path = '.\latent_true-true_dist.png'
        if not os.path.exists(output_file_path): #Check if the file already exists
            CreatePlot(distanceLatentBrute ,distanceTrue,PointIDs,title='Scatter Plot for distances',x_label='Query IDs',y_label='Distances',
                   scatter_labels=['Latent true dist','True dist'],output_file='latent_true-true_dist')
         
        CreatePlot(tLatentTrue ,tTrue,PointIDs,title='Scatter Plot for time',x_label='Query IDs',y_label='Time (ms)',
                   scatter_labels=['Latent True time','True time'],output_file='latent_true-true_time')    
        return []
    

    if normal_file == None:
        print("No normal file was imported!")
        return []

    PointIDs,distanceApprox,distanceBrute,tApprox,tTrue,aF = ReadFiles(normal_file)
    distanceApprox = list(map(float, distanceApprox))
    distanceBrute = list(map(float, distanceBrute))
    tApprox = list(map(float, tApprox))
    tTrue = list(map(float, tTrue))  
    aF_true = list(map(float, aF))
        #Create Distances Plot
    CreatePlot(distanceApprox,distanceBrute,PointIDs,title='Scatter Plot for distances',x_label='Query IDs',y_label='Distances',
                scatter_labels=['Approx Distances','True Distances'],output_file='approx-true_distances')
    
    CreatePlot(aF_Latent ,aF_true,PointIDs,title='Scatter Plot for Approximation Factor',x_label='Query IDs',y_label='Approximation Factor',
                scatter_labels=['Latent AF','True AF'],output_file='latent-true_AF',meanAF=True)
     
    ###CreatePlot(tApprox ,tTrue,PointIDs,title='Scatter Plot for time',x_label='Query IDs',y_label='Time (ms)',  We didnt need that plot at the end
    ###            scatter_labels=['Approx time','True time'],output_file='approx-true_time')

    
def CreatePlot(approx_vals,true_vals,query_ids,title,x_label,y_label,scatter_labels,output_file,colors = ['red','blue'],figsize = (10,6),meanAF=False):
        #Create Plot
        plt.figure(figsize=figsize)
        
        labels,values = [] , []
        if meanAF:
            mean_ratio_af = np.mean(approx_vals) / np.mean(true_vals)  #Calculate mean Latent AF and True AF
            labels = ['Mean ratio AF']
            values = [mean_ratio_af]
            plt.bar(labels, values, color=['purple']) #Inserting plt.bar into the existing plot
            if values:
                plt.text(0, values[0], f'{values[0]:.2f}', ha='center', va='bottom')

        plt.scatter(query_ids,approx_vals,label=scatter_labels[0],color=colors[0])
        plt.scatter(query_ids,true_vals,label=scatter_labels[1],color=colors[1])   
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.savefig(output_file)

latent_file,normal_file = None,None

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == '-l':
         latent_file = sys.argv[i + 1]
    elif sys.argv[i] == '-d':
        normal_file = sys.argv[i + 1]

if latent_file == None or normal_file == None:
    print("Missing input files!")
    exit(-1)

Plot(latent_file,normal_file,True)
Plot(latent_file,normal_file)






        

