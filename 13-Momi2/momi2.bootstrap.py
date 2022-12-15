import matplotlib.pyplot as plt
import momi
import logging
import pickle
import dill

logging.basicConfig(level=logging.INFO, filename="tutorial.bootstrap.log")

sfs = momi.Sfs.load("sfs.gz")

add_pulse_model = dill.load(open('best_run/add_pulse_model.txt', 'rb'))
results = pickle.load(open('best_run/results.txt', 'rb'))
best_result = pickle.load(open('best_run/best_result.txt', 'rb'))

add_pulse_model.set_params(best_result.parameters)

n_bootstraps = 1
# make copies of the original models to avoid changing them
#no_pulse_copy = no_pulse_model.copy()
add_pulse_copy = add_pulse_model.copy()

bootstrap_results = []
for i in range(n_bootstraps):
    print(f"Fitting {i+1}-th bootstrap out of {n_bootstraps}")
    # resample the data
    resampled_sfs = sfs.resample()
    # tell models to use the new dataset
    #no_pulse_copy.set_data(resampled_sfs)
    add_pulse_copy.set_data(resampled_sfs)
    # choose new random parameters for submodel, optimize
    #no_pulse_copy.set_params(randomize=True)
    #no_pulse_copy.optimize()
    # initialize parameters from submodel, randomizing the new parameters
    add_pulse_copy.set_params(randomize=True) #no_pulse_copy.get_params(),       
    add_pulse_copy.optimize()
    bootstrap_results.append(add_pulse_copy.get_params())

pickle.dump(bootstrap_results, open('bootstrap_results.txt', 'wb'))
