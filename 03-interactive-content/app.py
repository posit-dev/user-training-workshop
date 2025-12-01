from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Palmer Penguins dataset
try:
    penguins = sns.load_dataset("penguins")
    penguins = penguins.dropna()  # Remove rows with missing values
except:
    # Create sample data if seaborn dataset is not available
    import numpy as np
    np.random.seed(42)
    n = 300
    species = np.random.choice(['Adelie', 'Chinstrap', 'Gentoo'], n, p=[0.4, 0.3, 0.3])
    penguins = pd.DataFrame({
        'species': species,
        'island': np.random.choice(['Biscoe', 'Dream', 'Torgersen'], n),
        'bill_length_mm': np.random.normal(44, 5, n),
        'bill_depth_mm': np.random.normal(17, 2, n),
        'flipper_length_mm': np.random.normal(200, 15, n),
        'body_mass_g': np.random.normal(4200, 800, n),
        'sex': np.random.choice(['Male', 'Female'], n)
    })

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Filters"),
        ui.input_selectize(
            "species", 
            "Select Species:", 
            choices=list(penguins['species'].unique()),
            selected=list(penguins['species'].unique()),
            multiple=True
        ),
        ui.input_selectize(
            "island", 
            "Select Island:", 
            choices=list(penguins['island'].unique()),
            selected=list(penguins['island'].unique()),
            multiple=True
        ),
        ui.input_radio_buttons(
            "plot_type", 
            "Plot Type:",
            choices={
                "scatter": "Scatter Plot", 
                "histogram": "Histogram",
                "boxplot": "Box Plot"
            },
            selected="scatter"
        ),
        ui.input_select(
            "x_var", 
            "X Variable (for scatter):",
            choices={
                "bill_length_mm": "Bill Length",
                "bill_depth_mm": "Bill Depth", 
                "flipper_length_mm": "Flipper Length",
                "body_mass_g": "Body Mass"
            },
            selected="bill_length_mm"
        ),
        ui.input_select(
            "y_var", 
            "Y Variable (for scatter):",
            choices={
                "bill_length_mm": "Bill Length",
                "bill_depth_mm": "Bill Depth", 
                "flipper_length_mm": "Flipper Length",
                "body_mass_g": "Body Mass"
            },
            selected="flipper_length_mm"
        )
    ),
    ui.h2("Palmer Penguins Analysis"),
    ui.layout_columns(
        ui.card(
            ui.card_header("Data Visualization"),
            ui.output_plot("penguin_plot")
        ),
        ui.card(
            ui.card_header("Summary Statistics"),
            ui.output_table("summary_stats")
        ),
        col_widths=[8, 4]
    ),
    ui.card(
        ui.card_header("Data Preview"),
        ui.output_data_frame("data_preview")
    )
)

def server(input, output, session):
    @reactive.calc
    def filtered_data():
        # Filter data based on user selections
        data = penguins.copy()
        data = data[data['species'].isin(input.species())]
        data = data[data['island'].isin(input.island())]
        return data

    @render.plot
    def penguin_plot():
        data = filtered_data()
        
        if data.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'No data available for selected filters', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            return fig
        
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if input.plot_type() == "scatter":
            # Scatter plot
            for species in data['species'].unique():
                species_data = data[data['species'] == species]
                ax.scatter(species_data[input.x_var()], species_data[input.y_var()], 
                          label=species, alpha=0.7, s=50)
            
            ax.set_xlabel(input.x_var().replace('_', ' ').title())
            ax.set_ylabel(input.y_var().replace('_', ' ').title())
            ax.legend()
            
        elif input.plot_type() == "histogram":
            # Histogram
            for species in data['species'].unique():
                species_data = data[data['species'] == species]
                ax.hist(species_data[input.x_var()], alpha=0.7, label=species, bins=20)
            
            ax.set_xlabel(input.x_var().replace('_', ' ').title())
            ax.set_ylabel('Frequency')
            ax.legend()
            
        elif input.plot_type() == "boxplot":
            # Box plot
            species_list = data['species'].unique()
            box_data = [data[data['species'] == species][input.x_var()] for species in species_list]
            ax.boxplot(box_data, labels=species_list)
            ax.set_ylabel(input.x_var().replace('_', ' ').title())
        
        plt.title(f"Palmer Penguins - {input.plot_type().title()}")
        plt.tight_layout()
        return fig

    @render.table
    def summary_stats():
        data = filtered_data()
        
        if data.empty:
            return pd.DataFrame({"Message": ["No data available for selected filters"]})
        
        # Calculate summary statistics for numerical columns
        numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
        summary = data[numeric_cols].describe().round(2)
        summary.index.name = "Statistic"
        return summary

    @render.data_frame
    def data_preview():
        data = filtered_data()
        return data.head(20)  # Show first 20 rows

app = App(app_ui, server)
