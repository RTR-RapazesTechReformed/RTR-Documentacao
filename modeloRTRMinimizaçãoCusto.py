# Instalar Pulp, PuLP é um framework para modelagem e resolução de problemas
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "pulp"])

from pulp import *

# Importar gráfico
subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
import matplotlib.pyplot as plt
import numpy as np

# Variáveis
x = LpVariable("MManual", cat="Continuous", lowBound=1, upBound=10)
y = LpVariable("MOcr", cat="Continuous", lowBound=1, upBound=10)

# Problemas Lineares
prob = LpProblem("Minimização de custos")

# Objetivo e restrições
prob += 0.54*x + 0.10*y # função objetivo
prob += x+y >= 500
prob += x+y <= 2880
prob += x >= 0.4*(x+y)
prob += 0.1*y <= 30

# Resolver o modelo utilizando o método solve()
status = prob.solve()

# Mostrar o status da solução
LpStatus[status]

# Mostrar as variáveis e seus valores no meio do Prob
for var in prob.variables():
 print("{} = {}".format(var.name, var.varValue))
 print("custo min em BRL = ", pulp.value(prob.objective))

#Criar gráfico
x_val = x.varValue
y_val = y.varValue
custo = value(prob.objective)

# --- Plotando a região viável ---
x_range = np.linspace(0, 3000, 500)

# Restrições
y1 = 2880 - x_range               # x + y <= 2880
y2 = (3/2)*x_range                 # x >= 0.4(x+y) -> y <= 1.5x
y3 = 300 * np.ones_like(x_range)   # 0.1*y <= 30 -> y <= 300

plt.figure(figsize=(8,6))

# Região viável (interseção das restrições)
plt.fill_between(x_range, 0, np.minimum(np.minimum(y1, y2), y3), color='lightblue', alpha=0.5, label='Região viável')

# Ponto ótimo
plt.scatter(x_val, y_val, color='red', s=100, label='Solução ótima')

# Linhas das restrições
plt.plot(x_range, y1, label='x + y <= 2880')
plt.plot(x_range, y2, label='x >= 0.4*(x+y)')
plt.plot(x_range, y3, label='0.1*y <= 30')

plt.xlim(0, 3000)
plt.ylim(0, 350)
plt.xlabel('MManual (x)')
plt.ylabel('MOcr (y)')
plt.title('Região Viável e Solução Ótima')
plt.legend()
plt.grid(True)
plt.show()