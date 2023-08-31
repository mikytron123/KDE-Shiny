from shiny import App, ui, reactive, Inputs, Outputs, Session
from scipy.stats import norm, uniform, cauchy, chi2
import numpy as np
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget
from KDEpy import FFTKDE


dist_funcs = {
    "normal": norm(),
    "uniform": uniform(),
    "cauchy": cauchy(),
    "chi-square": chi2(4),
}


app_ui = ui.page_fluid(
    ui.panel_title("kernel density plots"),
    ui.layout_sidebar(
        sidebar=ui.panel_sidebar(
            ui.input_slider(
                "bw", "Bandwidth: ", min=0.001, max=1, value=0.1, step=0.01
            ),
            ui.input_selectize(
                "kernel",
                label="Select kernel",
                choices={
                    "gaussian": "Gaussian",
                    "biweight": "Biweight",
                    "epa": "Epanechnikov",
                    "tri": "Triangular",
                },
                selected="gaussian",
            ),
            ui.input_selectize(
                "distribution",
                label="Select distribution",
                choices=["normal", "uniform", "cauchy", "chi-square"],
            ),
        ),
        main=ui.panel_main(output_widget("render_plot")),
    ),
)


def server(input: Inputs, output: Outputs, session: Session) -> None:
    @reactive.Calc
    def calc_density() -> tuple[np.array, np.array]:
        dist = input.distribution()
        stat_gen = dist_funcs[dist]
        data = stat_gen.rvs(10000)
        mod = FFTKDE(kernel=input.kernel(), bw=input.bw()).fit(data)
        x, y = mod.evaluate()

        return x, y

    @output
    @render_widget
    def render_plot():
        x, y = calc_density()

        fig = go.FigureWidget(data=[go.Scatter(x=x, y=y, fill="tozeroy")])
        return fig


app = App(app_ui, server)
