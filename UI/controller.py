import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceCountry = None
        self._choiceCliente = None

    def handleCreaGrafo(self, e):
        if self._choiceCountry is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Selezionare un paese dal menu", color="red")
            )
            self._view.update_page()
            return
        self._model.creaGrafo(self._choiceCountry)
        nodi, archi = self._model.getDettagliGrafo()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato.", color="green")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Numero nodi: {nodi}")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Numero archi: {archi}")
        )
        self._fillDDCliente()
        self._view.update_page()


    def _fillDDCliente(self):
        clienti  = self._model.getAllClienti()
        for c in clienti:
            self._view._ddClienti.options.append(
                ft.dropdown.Option(data=c, text=c.LastName, on_click=self._saveChoiceDDCliente)
            )
        self._view.update_page()

    def _saveChoiceDDCliente(self,e):
        self._choiceCliente = e.control.data
        print(f"cliente: {self._choiceCliente}")
    def handleStampaInfo(self,e):
        clienteInf = self._model.stampaInfo()
        best5archi = self._model.best5archi()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Cliente più influente:{clienteInf[0]} - ({clienteInf[1]}).", color="green")
        )
        self._view._txt_result.controls.append(
            ft.Text(F"Top 5 archi con peso maggiore:")
        )
        counter = 1
        for a in best5archi:
            self._view._txt_result.controls.append(
                    ft.Text(f"{counter}. {a[0]} -> {a[1]} ({a[2]})")
                )
            counter += 1
        self._view.update_page()

    def handleSequenza(self,e):
        if self._choiceCliente is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Selezionare un cliente dal menu", color="red")
            )
            self._view.update_page()
            return
        listaFatt, fattComplessivo = self._model._getPath(self._choiceCliente)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Cammino con numero archi {len(listaFatt)-1} trovato. Di seguito i nodi che lo compongono", color="green")
        )

        for n in listaFatt:
            self._view._txt_result.controls.append(
                ft.Text(f"{n[0]} - {n[1]}")
            )
        self._view._txt_result.controls.append(
            ft.Text(f"Il fattirato complessivo del cammino è {fattComplessivo}",
                    color="green")
        )
        self._view.update_page()


    def fillDDCountries(self):
        countries = self._model.getAllCountries()
        for c in countries:
            self._view._ddCountry.options.append(
                ft.dropdown.Option(data=c,text=c,on_click=self._saveChoiceDDCountry)
            )
        self._view.update_page()

    def _saveChoiceDDCountry(self,e):
        self._choiceCountry = e.control.data
        print(f"Paese scelto: {self._choiceCountry}")