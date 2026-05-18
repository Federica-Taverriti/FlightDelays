from datetime import datetime
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza = None
        self._choiceArrivo = None

    def handleAnalizza(self, e):
        #chiamare metodo che crea grafo e stampare
        cMinTxt = self._view._txtInCMin.value
        if cMinTxt == "":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un valore numerico per numero minimo di compagnie.", color="red"))
            self._view.update_page()
            return

        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un valore intero per numero minimo di compagnie.", color="red"))
            self._view.update_page()
            return

        if cMin <= 0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Il filtro sul numero minimo di compagnie deve essere un intero positivo.", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(cMin)
        nNodes, nEdges = self._model.getGraphDetails()

        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)

        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text("Grafo correttamente creato:", color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi.", color="green"))
        self._view.update_page()


    def handleConnessi(self,e):
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza"))
            self._view.update_page()
            return

        viciniT = self._model.getViciniOrdinati(self._choicePartenza)
        self._view._txtResults.controls.clear()
        for v in viciniT:
            self._view._txtResults.controls.append(
                ft.Text(f"{v[0]} - peso: {v[1]}"))
        self._view.update_page()

    def handleTestConnessione(self,e):
        #verificare connessione esiste, se esiste trovare cammino qualsiasi
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza", color="red"))
            self._view.update_page()
            return

        if self._choiceArrivo is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di arrivo", color="red"))
            self._view.update_page()
            return

        if not self._model.hasPath(self._choicePartenza, self._choiceArrivo):
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text(f"Non ho trovato un cammino tra {self._choicePartenza} e {self._choiceArrivo}", color="orange"))
            self._view.update_page()
            return

        path = self._model.getPath(self._choicePartenza, self._choiceArrivo)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(f"Ho trovato un cammino tra {self._choicePartenza} e {self._choiceArrivo}"
                    f"Di seguito i nodi che compongono il cammino", color="green"))

        for p in path:
            self._view._txtResults.controls.append(ft.Text(p))
        self._view.update_page()

    def handleCerca(self,e):
        t = self._view._txtInNTratteMax.value

        try:
            tInt = int(t)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Il valore di t deve essere un intero positivo.", color="red"))
            return

        tic = datetime.now()
        path, score = self._model.getCamminoOttimo(self._choicePartenza, self._choiceArrivo, tInt)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(f"Cammino tra {self._choicePartenza} e {self._choiceArrivo} trovato", color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f"Il cammino ha uno score complessivo pari a {score} e contiene i seguenti nodi:", color="green"))

        for p in path:
            self._view._txtResults.controls.append(ft.Text(p), color="green")
            self._view._txtResults.controls.append(
                ft.Text(f"Cammino trovato in {datetime.now-tic}", color="green"))
        self._view.update_page()

    def _fillDropdown(self,allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data = n,
                                   key = n.IATA_CODE,
                                   on_click=self._choiceDdPartenza)
            )

        for n in allNodes:
            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(data = n,
                                   key = n.IATA_CODE,
                                   on_click=self._choiceDdArrivo)
            )

    def _choiceDdPartenza(self,e):
        self._choicePartenza = e.control.data
        print(f"Hai selezionato come aeroporto di partenza {self._choicePartenza}")

    def _choiceDdArrivo(self,e):
        self._choiceArrivo = e.control.data
        print(f"Hai selezionato come aeroporto di arrivo {self._choiceArrivo}")