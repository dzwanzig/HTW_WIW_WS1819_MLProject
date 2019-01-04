# Prolog - Auto Generated #
import os, matplotlib.pyplot, uuid, pandas
os.chdir(u'C:/Users/s0549851/PythonEditorWrapper_9b2cd701-d5b5-4e5c-98cb-77846ddfa627')
dataset = pandas.read_csv('input_df_e9a9331e-6181-4800-b684-7f38fc11899b.csv')

matplotlib.pyplot.figure(figsize=(5.55555555555556,4.16666666666667))
matplotlib.pyplot.show = lambda args=None,kw=None: matplotlib.pyplot.savefig(str(uuid.uuid1()))
# Original Script. Please update your script content here and once completed copy below section back to the original editing window #
import matplotlib.pyplot as plt

Nutzungsgradfaktor = (dataset.geplante_Produktionszeit - dataset.Nichtgeplante_Stillstaende) / dataset.geplante_Produktionszeit
Qualitätsfaktor = (dataset.produzierte_Menge - dataset.Ausschuss) / dataset.produzierte_Menge
Effizienzfaktor = dataset.produzierte_Menge / dataset.vorgegebene_Menge
OEE = Nutzungsgradfaktor * Qualitätsfaktor * Effizienzfaktor * 100

x=dataset.Datum
y=OEE

plt.plot(x, y, color="red")
plt.xlabel("Datum")
plt.ylabel("OEE in %")
plt.show()

# Epilog - Auto Generated #
os.chdir(u'C:/Users/s0549851/PythonEditorWrapper_9b2cd701-d5b5-4e5c-98cb-77846ddfa627')
