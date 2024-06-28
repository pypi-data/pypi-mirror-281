# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

color_rnd = ['blue', 'cyan', 'blueviolet', 'dodgerblue', 'teal', 'navy',
             'steelblue', 'deepskyblue', 'maroon', 'red', 'olivedrab', 'forestgreen',
             'olive', 'springgreen', 'limegreen', 'lawngreen', 'yellowgreen', 'green',
             ]



def plot_helper(ax,x,y,label,xlabel,ylabel,color='blue', linestyle='-.', marker='<', markersize=1, linewidth=1,**kwargs):

    ax.plot(x,y, label = label, color = color, marker = marker, 
            markersize = markersize, 
            linestyle = linestyle,
            linewidth = linewidth,**kwargs)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def scatter_helper(ax,x,y,label, xlabel, ylabel,color='blue', marker='+', markersize=10, **kwargs):

    ax.scatter(x,y, label = label, color = color, marker = marker,
             s = markersize,
             **kwargs)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def several_plots_helper(ax,xs,ys,labels,xlabels,ylabels,colors: list | None,markers : list | None, markersizes : list | None, **kwargs):
    '''
    Função para plotar diversos gráficos.

    PAREI AQUI
    '''
    if len(xs)!=len(ys):
        raise Exception('As dimensões das variáveis xs e ys devem ser iguais.')
    
    if len(labels)!=len(ys):
        raise Exception('A quantidade de labels deve ser igual à quantidade de ')
    

    pass





# %%

# %%
