import pandas as pd
from agent import run_agent

def main():
    print("Running crypto technical analysis agent...")
    df = run_agent(vs_currency="chf")

    output_file = "crypto_top20_ratings.csv"
    df.to_csv(output_file, index=False)

    print(f"Export complete → {output_file}")

if __name__ == "__main__":
    main()