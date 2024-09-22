import pandas as pd
import numpy as np

def printSaveScalars(sim_dir):
    print(f"\n \n---- print values in {sim_dir}/results/scalars.dat ----")
    # Reading and processing the names file
    names = pd.read_csv(f'{sim_dir}/results/scalars.dat.names', sep="+", header=None, skiprows=8)
    names.columns = ['variable']

    # Reading the data file
    data = np.loadtxt(f'{sim_dir}/results/scalars.dat')

    # Create a DataFrame for better structure and readability
    result = pd.DataFrame({'Variable': names['variable'], 'Value': data})
    # Print the matched variables and their values
    print(result.to_string(index=False))

if __name__ == "__main__":
    sim_dir = "./simdata/Case1"
    model = printSaveScalars(sim_dir)