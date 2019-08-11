import pulp, matplotlib.pyplot as plt, pandas as pd

df=pd.read_csv('DATA.csv')

data=df['column_title'].tolist()

simulation_days	=	7		
step_size		=	24		#1day
opti_horizon	=	24*2	#2day

r_A 			=	[0]
r_B 			=	[0]

for i in range(simulation_days):

	A={}
	B={}

	LP = pulp.LpProblem('LP',pulp.LpMaximize)

	for t in range(opti_horizon):

		A[t]=pulp.LpVariable("A_"+str(t), cat=pulp.LpContinuous, upBound=10, lowBound=0)
		B[t]=pulp.LpVariable("B_"+str(t), cat=pulp.LpContinuous, upBound=10, lowBound=0)

		if t==0:
			LP += 	A[t]		==	r_A[-1]
			LP += 	B[t]		==	r_B[-1]

		else:
			LP +=	A[t]	== 	A[t-1]	+	B[t]	*	data[t] 
			
	LP += sum([A[t] for t in range(opti_horizon)])

	status = LP.solve(pulp.solvers.CPLEX_PY(mip=True, msg=False, timeLimit=None, epgap=None))

	print( 'LP status: ' + pulp.LpStatus[status] + '')

	for t in range(step_size):
		r_A.append(A[t].value())
		r_B.append(B[t].value())

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(A,	color='r',	label="A")
ax1.plot(B,	color='g',	label="B")
ax2.plot(data[:simulation_days*step_size], color='b',	label="data")

ax1.legend(loc="upper left")
ax2.legend(loc="lower left")
plt.show()
