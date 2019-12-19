import numpy as np
import pandas as pd
import num_solver as ns

# The data used to solve BSEq.
test_data = pd.read_csv('HD_US_062918_C220_Equity.csv')

u_a, u_b = ns.u(test_data)
a_x = ns.find_ax(*ns.find_sab(test_data))
vola = ns.sigma(test_data)
init = ns.initial_value(np.polyval(u_a, 0), np.polyval(u_b, 0))

af_system = ns.system_af(u_a, u_b, a_x, vola, init, 20)

solution = ns.tikhonov(*af_system, 0.01)

B = np.reshape(solution, (20, 20))

f = open("output.txt", "w+")

print(B)

f.write(np.array2string(B))
f.close()
