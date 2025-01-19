import pandas as pd
import numpy as np

def validate_inputs(data, weights, impacts):
    # Validate  count
    if data.shape[1] < 3:
        raise ValueError("Input data must contain at least three columns.")
    
    # Validate numeric 
    if not all(data.iloc[:, 1:].applymap(lambda x: isinstance(x, (int, float))).all()):
        raise ValueError("All columns from the 2nd to last must contain numeric values only.")
    
    # Parse weights and impacts
    try:
        weights = [float(w) for w in weights.split(",")]
    except ValueError:
        raise ValueError("Weights must be numeric values separated by commas.")
    
    impacts = impacts.split(",")
    if len(weights) != data.shape[1] - 1 or len(impacts) != data.shape[1] - 1:
        raise ValueError("The number of weights and impacts must match the number of numeric columns.")
    
    if not all(i in ['+', '-'] for i in impacts):
        raise ValueError("Impacts must be '+' or '-'.")
    
    return weights, impacts

def topsis(data, weights, impacts):
    # step 1 : Normalize 
    normalized_data = data.iloc[:, 1:].div(np.sqrt((data.iloc[:, 1:] ** 2).sum()), axis=1)

    # step 2 : Apply weights
    weighted_data = normalized_data * weights

    # step 3 : Determine ideal best and worst
    ideal_best = [weighted_data.iloc[:, i].max() if impacts[i] == '+' else weighted_data.iloc[:, i].min() for i in range(len(impacts))]
    ideal_worst = [weighted_data.iloc[:, i].min() if impacts[i] == '+' else weighted_data.iloc[:, i].max() for i in range(len(impacts))]

    # step 4 : Calculate distances
    distance_to_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    distance_to_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # step 5 : Calculate Topsis score
    scores = distance_to_worst / (distance_to_best + distance_to_worst)

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