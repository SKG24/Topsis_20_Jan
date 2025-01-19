import sys
import pandas as pd
import numpy as np

#-----------VALIDATE FUNCTION-----------------------
def validate_inp(input_file, wght, impacts, result_file):
    # Validate file
    try:
        if input_file.endswith('.xlsx'):
            data = pd.read_excel(input_file)
        else:
            data = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unable to read the file '{input_file}'. {e}")
        sys.exit(1)

    # Validate column count
    if data.shape[1] < 3:
        print("Error: Input file must contain at least three columns.")
        sys.exit(1)

    # Validate numeric columns
    if not all(data.iloc[:, 1:].applymap(lambda x: isinstance(x, (int, float))).all()):
        print("Error: All columns from the 2nd to last must contain numeric values only.")
        sys.exit(1)

    # Validate weights and impacts length
    try:
        wght = [float(w) for w in wght.split(",")]
    except ValueError:
        print("Error: Weights must be numeric values separated by commas.")
        sys.exit(1)

    impacts = impacts.split(",")

    if len(wght) != data.shape[1] - 1 or len(impacts) != data.shape[1] - 1:
        print("Error: The number of weights and impacts must match the number of columns from the 2nd to the last in the input file.")
        sys.exit(1)

    # Validate impacts
    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must be either '+' or '-'.")
        sys.exit(1)

    return data, wght, impacts

#-----------TOPSIS FUNCTION -----------------------
def topsis(data, wght, impacts):
    # step 1 : Normalize 
    normalized_data = data.iloc[:, 1:].div(np.sqrt((data.iloc[:, 1:] ** 2).sum()), axis=1)

    # step 2 : Apply weight
    weighted_data = normalized_data * wght

    # step 3 : ideal best and worst
    ideal_best = []
    ideal_worst = []
    for i, impact in enumerate(impacts):
        if impact == '+':
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())

    # step 4 : Calculate distances
    dst_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dst_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # step 5 : Calculate Topsis score
    scores = dst_worst / (dst_best + dst_worst)

    return scores

def main():
    print("This is written by Sanat Kumar Gupta 102203079 3C52")
    if len(sys.argv) != 5:
        print("How to use: python <program.py> <InputDataFile> <weigth> <Impacts> <ResultFileName> ... for macos use python3")
        sys.exit(1)

    input_file = sys.argv[1]
    wght = sys.argv[2]
    impacts = sys.argv[3]
    result_file = sys.argv[4]

    # Validate 
    data, wght, impacts = validate_inp(input_file, wght, impacts, result_file)

    # Calculate 
    scores = topsis(data, wght, impacts)

    # Rank 
    data['Topsis Score'] = scores
    data['Rank'] = scores.rank(ascending=False).astype(int)

    # Save 
    try:
        data.to_csv(result_file, index=False)
        print(f"Result file '{result_file}' generated successfully.")
    except Exception as e:
        print(f"Error: Could not write to file '{result_file}'. {e}")

if __name__ == "__main__":
    main()
