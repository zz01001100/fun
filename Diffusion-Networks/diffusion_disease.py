import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep

# Dein Code
g = nx.erdos_renyi_graph(1000, 0.1)
model = ep.SIRModel(g)
cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.01)
cfg.add_model_parameter('gamma', 0.005)
cfg.add_model_parameter("fraction_infected", 0.05)
model.set_initial_status(cfg)
iterations = model.iteration_bunch(10000)

# Trends extrahieren
trends = model.build_trends(iterations)

# Die Verläufe für jeden Zustand holen (0=S, 1=I, 2=R)
s_verlauf = trends[0]['trends']['node_count'][0]
i_verlauf = trends[0]['trends']['node_count'][1]
r_verlauf = trends[0]['trends']['node_count'][2]

# --- FORMATIERTER OUTPUT ---
print(f"Das Netzwerk startet mit 1000 Personen, wovon 5% ({int(i_verlauf[0])} Personen) infiziert sind.")
print(f"Die Infektionsrate (beta) liegt bei 1.0% und die Genesungsrate (gamma) bei 0.5%.")
print(f"Wir simulieren die Ausbreitung über 200 Zeitschritte.")
print("\nDies führt zu folgenden Ergebnissen im Endstand:")
print(f"Gesund (S):    {int(s_verlauf[-1])}")
print(f"Infiziert (I): {int(i_verlauf[-1])}")
print(f"Genesen (R):   {int(r_verlauf[-1])}")
