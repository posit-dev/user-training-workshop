from shiny import App, render, ui, reactive
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Palmer Penguins dataset
penguins = sns.load_dataset("penguins").dropna()

# Numeric variables available for plotting
VARS = {
    "bill_length_mm": "Bill Length",
    "bill_depth_mm": "Bill Depth",
    "flipper_length_mm": "Flipper Length",
    "body_mass_g": "Body Mass",
}

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Filters"),
        ui.input_selectize(
            "species", "Select Species:",
            choices=sorted(penguins["species"].unique()),
            selected=sorted(penguins["species"].unique()),
            multiple=True,
        ),
        ui.input_selectize(
            "island", "Select Island:",
            choices=sorted(penguins["island"].unique()),
            selected=sorted(penguins["island"].unique()),
            multiple=True,
        ),
        ui.input_radio_buttons(
            "plot_type", "Plot Type:",
            choices={"scatter": "Scatter Plot", "histogram": "Histogram", "boxplot": "Box Plot"},
        ),
        ui.input_select("x_var", "X Variable:", choices=VARS, selected="bill_length_mm"),
        ui.input_select("y_var", "Y Variable:", choices=VARS, selected="flipper_length_mm"),
    ),
    ui.h2("COOOOOL PENGUINS!!!!!!"),
    ui.card(ui.card_header("Data Visualization"), ui.output_plot("penguin_plot")),
)


def server(input, output, session):
    @reactive.calc
    def filtered_data():
        return penguins[
            penguins["species"].isin(input.species())
            & penguins["island"].isin(input.island())
        ]

    @render.plot
    def penguin_plot():
        data = filtered_data()
        fig, ax = plt.subplots(figsize=(10, 6))

        if data.empty:
            ax.text(0.5, 0.5, "No data available for selected filters",
                    ha="center", va="center", fontsize=14)
            ax.axis("off")
            return fig

        x, y = input.x_var(), input.y_var()
        if input.plot_type() == "scatter":
            sns.scatterplot(data=data, x=x, y=y, hue="species", alpha=0.7, ax=ax)
            ax.set(xlabel=VARS[x], ylabel=VARS[y])
        elif input.plot_type() == "histogram":
            sns.histplot(data=data, x=x, hue="species", bins=20, ax=ax)
            ax.set(xlabel=VARS[x])
        else:  # boxplot
            sns.boxplot(data=data, x="species", y=y, ax=ax)
            ax.set(ylabel=VARS[y])

        ax.set_title(f"Palmer Penguins - {input.plot_type().title()}")
        return fig


app = App(app_ui, server)
