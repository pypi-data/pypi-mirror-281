from SimLogger import SimLogger
import figurl as fig
import plotly.express as px
import pandas as pd
import os

def createPlot(simTag, objTag, x, y, objFolder=os.path.join('data','obj'),  z=None, plot_type='scatter', title='Plot', makeNote=True, **kwargs):
    
    data = {'x': x, 'y': y}
    if z is not None:
        data['z'] = z
    
    df = pd.DataFrame(data)

    if plot_type == 'scatter':
        if z is not None:
            fig = px.scatter_3d(df, x='x', y='y', z='z', title=title, **kwargs)
        else:
            fig = px.scatter(df, x='x', y='y', title=title, **kwargs)
    elif plot_type == 'line':
        fig = px.line(df, x='x', y='y', title=title, **kwargs)
    else:
        raise ValueError("Unsupported plot_type. Supported types: 'scatter', 'line'.")

    savePlotly(simTag, objTag, fig, label=title, objFolder=objFolder, makeNote=makeNote)
    
def savePlotly(simTag, objTag, ff, label='', objFolder=os.path.join('data','obj'), makeNote=True):
    if label=='': label=objTag
    url = fig.Plotly(ff).url(label=label)
    SimLogger.logNotes(f'{label} GRAPH AVAILABLE AT: {url}')
    SimLogger.saveObj(simTag, objTag, ff, objFolder=objFolder, makeNote=makeNote)

    return url
