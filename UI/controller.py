import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph()
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di Nodes: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di Edges: {nEdges}"))
        self._view.txt_result.controls.append(ft.Text(
            f"Informazioni sui pesi degli archi - valore minimo:  {self._model.getMinWeight()} e valore massimo: {self._model.getMaxWeight()}"
        ))
        self._view.update_page()
    def handle_countedges(self, e):
        soglia = float(self._view.txt_name.value)
        if soglia < self._model.getMinWeight() or soglia > self._model.getMaxWeight():
            self._view.create_alert("Valore di soglia non valida!")
            return
        count_bigger, count_smaller = self._model.countEdges(soglia)
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia: {count_bigger}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso minore della soglia: {count_smaller}"))
        self._view.update_page()

    def handle_search(self, e):
        threshold = float(self._view.txt_name.value)
        self._model.searchPath(threshold)

        self._view.txt_result3.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.computeWeightPath(self._model.solBest))}"))

        for ii in self._model.solBest:
            self._view.txt_result3.controls.append(ft.Text(
                f"{ii[0]} --> {ii[1]}: {str(ii[2]['weight'])}"))
        self._view.update_page()