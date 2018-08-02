import plotly.graph_objs as go
import colorlover as cl

def get_axis_template():
    return dict(
        ticks='',
        showgrid=False,
        zeroline=False,
        showline=True,
        mirror=True,
        linewidth=2,
        linecolor='#444',
    )

def get_layout(title, width, height):
    return go.Layout(xaxis=get_axis_template(),
                     yaxis=get_axis_template(),
                     width=width,
                     height=height,
                     autosize=False,
                     hovermode='closest',
                     title=title)

def get_colorscale(colorscale='Blues'):
    """
    Getting colorscale
    :param colorscale: 'RdYlBu', 'Blues', 'Reds', 'Greens', 'YlOrRd',
    'RdPu', 'YlOrBr', 'YlGnBu', 'GnBu', 'BuPu', 'Greys', 'Oranges',
    'OrRd', 'BuGn', 'PuBu', 'PuRd', 'PuBuGn', 'YlGn', 'Purples'.
    :return: colorscale
    """
    scl = cl.scales['9']['seq'][colorscale]
    return [ [ float(i)/float(len(scl)-1), scl[i] ] for i in range(len(scl)) ]
