# Importar bibliotecas utilizadas

import matplotlib.pyplot as plt
import mplcyberpunk

# Definir variáveis para cálculo
capitalInicial = 100000
taxaJuros = 0.12
periodo = 30
periodo = int(periodo)

# Definir função para calcular juros compostos
def calculaMontante(capitalInicial, taxaJuros, periodo):
    montante = capitalInicial * (1 + taxaJuros) ** periodo
    return montante


# Definir lista de anos para calcular
periodosLista = periodo + 1
anos = list(range(periodosLista))

# Definir todos os montantes calculados dentro da lista de resultados
montantes = [calculaMontante(capitalInicial, taxaJuros, periodo) for periodo in anos]
print(montantes)

# Personalizar tema do gráfico
plt.style.use("cyberpunk")

# Definir quais informações serão mostradas no gráfico
plt.plot(anos, montantes)
plt.xlabel("Anos")
plt.ylabel("Montante")
plt.title("Juros Compostos")
ax = plt.gca()
ax.ticklabel_format(style='plain', axis='both')


# Mostrar gráfico com cálculo
plt.show()