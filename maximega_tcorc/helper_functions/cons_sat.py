import z3

def cons_sat(data_copy, k):
    parameter_names_z = ["z{0:d}".format(i) for i in range(1, k + 1)]
    parameters_z = [z3.Real(n) for n in parameter_names_z]
    S = z3.Solver()
    #(set-option :pp-decimal true)
    #S.set_option(precision = 3)
    #(set-option :pp-decimal-precision 2)
    totals_projected = [0] * k
    avg_inc = [0] * k
    count_inc = [0] * k
    overall_total_real = 0
    for item in data_copy:
        totals_projected[item['zone']] += float(item['population']) * (item['trans_percent'] / 100)
        overall_total_real += float(item['population']) * (item['trans_percent'] / 100) * 2.75


    overall_total_real = int(overall_total_real)

    val = 0
    for i in range(k):
        val += (parameters_z[i] * totals_projected[i])
    S.add(val == int(overall_total_real))

    for i in range(len(parameters_z)):
        val = (parameters_z[i] * totals_projected[i])/overall_total_real
        S.add(val < .4, val > .05)
    S.add(parameters_z[0] < parameters_z[1],  parameters_z[1] < parameters_z[2])
    S.add(parameters_z[2] < parameters_z[3], parameters_z[3] < parameters_z[4])
    S.add(parameters_z[0] * 1.25 > parameters_z[4])
    
    print(S.check())
    print(S.model())
    