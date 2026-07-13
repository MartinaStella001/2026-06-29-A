from model.model import Model

mdl= Model()
mdl.creaGrafo("USA")
nodi, archi = mdl.getDettagliGrafo()
print(f"nodi : {nodi}, archi: {archi}")
