import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import warnings
warnings.filterwarnings('ignore')
#ITCRM

tcrm = pd.read_excel(r'C:\Users\rumtl\PycharmProjects\Macro Reaserch\ITCRMSerie (2).xls')
tcrm.rename(columns={"Unnamed: 0":"Fecha", "Índices con base 17-12-15=100":"ITCRM"}, inplace=True)
tcrm.drop(0, inplace=True)
itcrm = tcrm[["Fecha", "ITCRM"]]
itcrm.dropna(inplace=True)
itcrm["Fecha"] = pd.to_datetime(itcrm["Fecha"])
itcrm.set_index("Fecha", inplace=True)


#Tipo de cambio A3500

dlr_oficial = pd.read_excel(r'C:\Users\rumtl\PycharmProjects\Macro Reaserch\com3500 (40).xls')
dlr_oficial.rename(columns={"Unnamed: 2":"Fecha", "Unnamed: 3":"dlr"}, inplace=True)
dlr_oficial.drop([0,1,2], inplace=True)
dlr_oficial2 = dlr_oficial[["Fecha", "dlr"]].set_index("Fecha")

#Tipo de cambio CCL

ggal_pesos = yf.download("GGAL.BA", start="2019-01-05", end=dt.date.today())
ggal_ba = ggal_pesos[["Adj Close"]].rename(columns={"Adj Close":"ggal_$"})

ggal_adr = yf.download("GGAL", start="2019-01-05", end=dt.date.today())
ggal_ny = ggal_adr[["Adj Close"]].rename(columns={"Adj Close":"ggal_usd"})

ccl = pd.merge(left=ggal_ba, right=ggal_ny, how="inner",
                left_on="Date", right_on="Date")

ccl["CCL"] = ccl["ggal_$"] * 10 / ccl["ggal_usd"]

ccl = ccl[["CCL"]]

#Tipo de cambio CCL
ggal_pesos = yf.download("GGAL.BA", start="2019-01-05", end=dt.date.today())
ggal_ba = ggal_pesos[["Adj Close"]].rename(columns={"Adj Close":"ggal_$"})

ggal_adr = yf.download("GGAL", start="2019-01-05", end=dt.date.today())
ggal_ny = ggal_adr[["Adj Close"]].rename(columns={"Adj Close":"ggal_usd"})

ccl = pd.merge(left=ggal_ba, right=ggal_ny, how="inner",
                left_on="Date", right_on="Date")

ccl["CCL"] = ccl["ggal_$"] * 10 / ccl["ggal_usd"]

ccl = ccl[["CCL"]]

#Ratio CCL/Oficial
ratio = pd.merge(left=ccl, right=dlr_oficial2, how="inner",
                 left_on=ccl.index, right_on="Fecha").set_index("Fecha")


ratio["ratio_total"] = ratio["CCL"] / ratio["dlr"]

adj_itcrm = pd.merge(left=ratio, right=itcrm, how="inner",
                     left_on="Fecha", right_on="Fecha")

adj_itcrm["itcrm_ccl"] = adj_itcrm["ITCRM"] * adj_itcrm["ratio_total"]

#Grafico

plt.rcParams["figure.figsize"] = [12,6]

plt.plot(itcrm["ITCRM"], c="g", lw=0.75, label="ITCRM oficial")
plt.plot(adj_itcrm["itcrm_ccl"].loc["2019-06-01":], c="r", lw=1,
         label="Ajustado por ccl")
plt.axhline(adj_itcrm["itcrm_ccl"][-1], ls="dotted", lw=0.75, c="r")
# Devaluaciones mayores a 20% en un día
plt.axvline(x = ["2002-03-24"], ls="dashdot", lw=0.75, c="b")
plt.axvline(x = ["2002-01-06"], ls="dashdot", lw=0.75, c="b")
plt.axvline(x = ["2015-12-17"], ls="dashdot", lw=0.75, c="b")
plt.axvline(x = ["2018-08-30"], ls="dashdot", lw=0.75, c="b")
plt.axvline(x = ["2019-08-12"], ls="dashdot", lw=0.75, c="b")


plt.legend(loc=2)
plt.title("Indice de Tipo de Cambio Real Multilateral")
#Si se quiere guardar la imagen:
plt.savefig(r'C:\Users\rumtl\PycharmProjects\Macro Reaserch\itcrm2.png',
              bbox_inches='tight')

plt.show()
