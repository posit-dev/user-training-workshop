import pandas as pd
import matplotlib.pyplot as plt
import time

def main():
    print("Loading weather data...")
    time.sleep(5)

    # Load data
    df = pd.read_csv('weather.csv')
    print(f"Loaded {len(df)} records")
    time.sleep(3)

    print("Analyzing temperature patterns...")
    time.sleep(8)

    # Basic statistics
    avg_temp = df['temperature_f'].mean()
    max_temp = df['temperature_f'].max()
    min_temp = df['temperature_f'].min()

    print(f"Average temperature: {avg_temp:.1f}°F")
    print(f"Temperature range: {min_temp:.1f}°F to {max_temp:.1f}°F")
    time.sleep(5)

    print("Creating visualization...")
    time.sleep(8)

    # Create simple plot
    plt.figure(figsize=(10, 6))
    df.boxplot(column='temperature_f', by='weather_condition')
    plt.title('Temperature Distribution by Weather Condition')
    plt.suptitle('')
    plt.xticks(rotation=45)
    plt.tight_layout()

    print("Saving plot...")
    time.sleep(5)
    plt.savefig('weather_plot_py.png')

    print("Generating summary statistics...")
    time.sleep(8)

    # Weather condition summary
    summary = df.groupby('weather_condition')['temperature_f'].agg(['mean', 'count']).round(1)
    print("\nWeather Summary:")
    print(summary)

    print("Saving results...")
    time.sleep(3)
    summary.to_csv('weather_summary_py.csv')

    print("Analysis complete! Files saved: weather_plot_py.png, weather_summary_py.csv")

if __name__ == "__main__":
    main()
