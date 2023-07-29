from shiny import App, render, ui,reactive,Inputs,Outputs,Session
from scipy.stats import norm
import numpy as np
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget
from KDEpy import FFTKDE

app_ui = ui.page_fluid(
    ui.panel_title("kernel density plots"),
    ui.layout_sidebar(
        sidebar=ui.panel_sidebar(
            ui.input_slider("bw", "Bandwidth: ", min=0.001, max=1, value=0.1,step=0.01),
            ui.input_select("kernel",label="Select kernel",
                    choices={'gaussian': 'Gaussian',
                            'biweight': 'Biweight',
                            'epa': 'Epanechnikov',
                            'tri': 'Triangular'},selected="gaussian")
            
        ),

        main=ui.panel_main(output_widget("render_plot"))
    )
)


def server(input:Inputs, output:Outputs, session:Session)->None:

    @reactive.Calc
    def calc_density()-> tuple[np.array,np.array]: # type: ignore
        data = norm().rvs(10000)
        mod = FFTKDE(kernel=input.kernel(),bw=input.bw()).fit(data) # type: ignore
        dens_x = np.linspace(start=np.min(data),stop=np.max(data),num=10000)
        x, y = mod.evaluate()
        
        # dens = sm.nonparametric.KDEUnivariate(data)
        # fft=False
        # if input.kernel()=="gau":
        #     fft=True
        # dens.fit(kernel=input.kernel(),fft=fft)
        return x,y




    # @output
    # @render.text
    # def selected_choice():
    #     return f"the kernel is {input.kernel()}"
    
    @output
    @render_widget
    def render_plot():
        x,y = calc_density()

        fig = go.FigureWidget(data=[go.Scatter(x=x,y=y,fill="tozeroy")])
        return fig
    


app = App(app_ui, server)
