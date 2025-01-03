import pandas

from gsgp.GSGP import GSGP
from sys import argv
from Arguments import *
import os

from sklearn.model_selection import train_test_split

import numpy as np


# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-GSGP
#
# Copyright ©2019-2023 J. E. Batista
#

# This has been modified for E Mackness' dissertation research

def openAndSplitDatasets(which, seed):
    if VERBOSE:
        print("> Opening: ", which)

    # Open dataset
    ds = pandas.read_csv(DATASETS_DIR + which)

    # Read header
    class_header = ds.columns[-1]

    return train_test_split(ds.drop(columns=[class_header]), ds[class_header],
                            train_size=TRAIN_FRACTION, random_state=seed,
                            stratify=ds[class_header])


def run(r, dataset):
    if VERBOSE:
        print("> Starting run:")
        print("  > ID:", r)
        print("  > Dataset:            " + dataset)
        print()

    Tr_X, Te_X, Tr_Y, Te_Y = openAndSplitDatasets(dataset, r)

    # Train a model
    model = GSGP(OPERATORS, MAX_DEPTH, POPULATION_SIZE, MAX_GENERATION, TOURNAMENT_SIZE,
                 ELITISM_SIZE, MUTATION_STEP, THREADS, r, VERBOSE)
    model.fit(Tr_X, Tr_Y, Te_X, Te_Y)

    # Obtain training results
    accuracy = model.getAccuracyOverTime()
    waf = model.getWaFOverTime()
    kappa = model.getKappaOverTime()
    mse = model.getRMSEOverTime()
    model_str = model.getBestIndividualRepresentation()
    times = model.getGenerationTimes()

    tr_acc = accuracy[0]
    te_acc = accuracy[1]
    tr_waf = waf[0]
    te_waf = waf[1]
    tr_kappa = kappa[0]
    te_kappa = kappa[1]
    tr_mse = mse[0]
    te_mse = mse[1]

    if VERBOSE:
        print("> Ending run:")
        print("  > ID:", r)
        print("  > Dataset:", dataset)
        print("  > Final model:", model_str)
        print("  > Training accuracy:", tr_acc[-1])
        print("  > Test accuracy:", te_acc[-1])
        print()

    return (tr_acc, te_acc,
            tr_waf, te_waf,
            tr_kappa, te_kappa,
            tr_mse, te_mse,
            times,
            model_str)


def callGSGP():
    try:
        # Makes the results folder, if it doesn't exist
        os.makedirs(OUTPUT_DIR)
    except FileExistsError:
        pass

    for dataset in DATASETS:
        outputFilename = OUTPUT_DIR + "GSGP_" + dataset
        if not os.path.exists(outputFilename):
            results = []

            # Run the algorithm several times
            for r in range(RUNS):
                results.append(run(r, dataset))

                #    The result file is update after every run to
                # avoid losing information if the program crashes

                # Write output header
                file = open(outputFilename, "w")
                file.write("Attribute,Run,")
                for i in range(MAX_GENERATION):
                    file.write(str(i) + ",")
                file.write("\n")

                attributes = ["Training-Accuracy", "Test-Accuracy",
                              "Training-WaF", "Test-WaF",
                              "Training-Kappa", "Test-Kappa",
                              "Training-RMSE", "Test-RMSE",
                              "Time",
                              "Final_Model"]

                # Write attributes with value over time
                for ai in range(len(attributes) - 1):
                    for i in range(len(results)):
                        file.write("\n" + attributes[ai] + "," + str(i) + ",")
                        file.write(",".join([str(val) for val in results[i][ai]]))
                    file.write("\n")

                # Write the final models
                for i in range(len(results)):
                    file.write("\n" + attributes[-1] + "," + str(i) + ",")
                    file.write(results[i][-1])
                file.write("\n")

                # Write some parameters
                file.write("\n\nParameters")
                file.write("\nOperators," + str(OPERATORS))
                file.write("\nMax Initial Depth," + str(MAX_DEPTH))
                file.write("\nPopulation Size," + str(POPULATION_SIZE))
                file.write("\nMax Generation," + str(MAX_GENERATION))
                file.write("\nTournament Size," + str(TOURNAMENT_SIZE))
                file.write("\nElitism Size," + str(ELITISM_SIZE))
                file.write("\nThreads," + str(THREADS))
                file.write("\nRandom State," + str(list(range(RUNS))))
                file.write("\nDataset," + dataset)

                file.close()

        else:
            # If the result file already exists, GSGP won't run.
            print("Filename: " + outputFilename + " already exists.")


if __name__ == '__main__':
    callGSGP()
