import matplotlib.pyplot as plt
import momi
import logging
import pickle
import dill
logging.basicConfig(level=logging.INFO, filename="tutorial.log")

sfs = momi.Sfs.load("sfs.gz")
add_pulse_model = momi.DemographicModel(N_e=1e3, gen_time=3, muts_per_gen=5.4e-9)
add_pulse_model.set_data(sfs)

add_pulse_model.add_size_param("n_weug",lower=500,upper=1e6)
add_pulse_model.add_size_param("n_weue",lower=500,upper=1e6)
add_pulse_model.add_size_param("n_ceug",lower=500,upper=1e6)
add_pulse_model.add_size_param("n_ceua",lower=500,upper=1e6)

add_pulse_model.add_time_param("t_weue_ceug", lower=8.95e3,upper=1.54e4)
add_pulse_model.add_time_param("t_ceug_ceua", lower=7.74e3,upper=1.14e4,upper_constraints=["t_weue_ceug"])
add_pulse_model.add_time_param("t_weue_weug", lower=3.69e5,upper=3.98e5)

add_pulse_model.add_leaf("CEUA", N="n_ceua")
add_pulse_model.add_leaf("CEUG", N="n_ceug")
add_pulse_model.add_leaf("WEUE", N="n_weue")
add_pulse_model.add_leaf("WEUG", N="n_weug")


add_pulse_model.move_lineages("CEUA", "CEUG", t="t_ceug_ceua",p=1)
add_pulse_model.move_lineages("CEUG", "WEUE", t="t_weue_ceug",p=1)
add_pulse_model.move_lineages("WEUG", "WEUE", t="t_weue_weug",p=1)

#adding a WEUG->CEUA migration arrow.
add_pulse_model.add_pulse_param("weug_ceua_pulse", upper=.5)
add_pulse_model.add_time_param("t_weug_ceua_pulse", upper_constraints=["t_ceug_ceua"])
add_pulse_model.move_lineages("CEUA", "WEUG", t="t_weug_ceua_pulse", p="weug_ceua_pulse")

results = []
n_runs = 1
for i in range(n_runs):
    print(f"Starting run {i+1} out of {n_runs}...")
    add_pulse_model.set_params(
        # parameters inherited from no_pulse_model are set to their previous values
        # no_pulse_model.get_params(),
        # other parmaeters are set to random initial values
        randomize=True)
#    results.append(add_pulse_model.optimize(method="L-BFGS-B",options={"maxiter":200}))
    results.append(add_pulse_model.optimize(method="TNC",options={"maxiter":200}))

dill.dump(add_pulse_model, open('add_pulse_model.txt', 'wb'))
pickle.dump(results, open('results.txt', 'wb'))
best_result = results[0]
print(best_result)
pickle.dump(best_result, open('best_result.txt', 'wb'))

add_pulse_model.set_params(best_result.parameters)

yticks = [1e3,1e4, 2.5e4, 5e4, 7.5e4, 1e5, 2.5e5, 5e5]
fig = momi.DemographyPlot(
    add_pulse_model, ["WEUE", "CEUG", "CEUA","WEUG"],
    figsize=(8,10),
    major_yticks=yticks,
    linthreshy=1e3, pulse_color_bounds=(0,.5))
plt.savefig("WEUE_CEUG_CEUA_WEUG.pdf")

#fig.draw_N_legend(loc="upper right")

