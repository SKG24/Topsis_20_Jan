import sys
import pandas as pd
import numpy as np

def validate_inputs(data, weights, impacts):
    # Your validation logic here
    if len(data.columns) < 3:
        raise ValueError("Input data must contain at least three columns.")
    if len(weights) != len(data.columns):
        raise ValueError("Number of weights must match the number of criteria.")
    if len(impacts) != len(data.columns):
        raise ValueError("Number of impacts must match the number of criteria.")
    if not all(isinstance(w, (int, float)) for w in weights):
        raise ValueError("All weights must be numeric.")
    if not all(i in ['+', '-'] for i in impacts):
        raise ValueError("Impacts must be either '+' or '-'.")

def topsis(data, weights, impacts):
    # Normalization
    normalized_data = data / np.sqrt((data**2).sum())
    
    # Weighting
    weighted_data = normalized_data * weights
    
    # Ideal and Negative Ideal Solutions
    ideal_best = np.where(impacts == '+', weighted_data.max(), weighted_data.min())
    ideal_worst = np.where(impacts == '+', weighted_data.min(), weighted_data.max())
    
    # Distance Calculation
    distance_best = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))
    
    # Topsis Score
    scores = distance_worst / (distance_best + distance_worst)
    
    # Append results
    data['Topsis Score'] = scores
    data['Rank'] = scores.rank(ascending=False).astype(int)
    return data

def main():
    if len(sys.argv) != 4:
        print("Usage: topsis <csv_filename> <weights_vector> <impacts_vector>")
        sys.exit(1)

    csv_filename = sys.argv[1]
    weights_vector = sys.argv[2]
    impacts_vector = sys.argv[3]

    data = pd.read_csv(csv_filename)
    weights = [float(w) for w in weights_vector.split(',')]
    impacts = impacts_vector.split(',')

    validate_inputs(data, weights, impacts)
    result = topsis(data, weights, impacts)
    
    print("TOPSIS RESULTS")
    print("-----------------------------")
    print(result)

if __name__ == "__main__":
    main()