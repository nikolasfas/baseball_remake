import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._year = None
        self._teams = []
        self._choiceTeam = None

    def handleCreaGrafo(self, e):
        self._model.buildGraph()
        nodes, edges = self._model._getGraphDetails()
        self._view._txt_result.controls.append(
            ft.Text(f"Graph successfully created: {len(nodes)} nodes, {len(edges)} edges")
        )

        self._view.update_page()

    def handleChoiceTeam(self, e):
        selected_name = e.control.value

        for team in self._teams:
            if team.name == selected_name:
                self._choiceTeam = team
                break

    def handleDettagli(self, e):
        neighbours = self._model.getNeighbours(self._choiceTeam)

        self._view._txt_result.controls.append(
            ft.Text(f"For {self._choiceTeam}, the neighbours are: ")
        )
        for n in neighbours:
            self._view._txt_result.controls.append(
                ft.Text(f"{n[1]} - {n[0]}")
            )

        self._view.update_page()

    def handlePercorso(self, e):
        path, value = self._model.handlePercorso(self._choiceTeam)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Il percorso trovato ha peso {value}, e comprende i seguenti nodi: ")
        )

        for i in range(len(path)-1):
            n1 = path[i]
            n2 = path[i+1]
            peso = self._model.getEdgeWeight(n1, n2)
            self._view._txt_result.controls.append(
                ft.Text(f"{n1} -> {n2} - {peso}")
            )

        self._view.update_page()

    def handleTeams(self, e):
        self._year = int(e.control.value)
        self._teams = self._model.getAllTeams(self._year)

        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"I've found {len(self._teams)} teams which are playing in the {self._year} season: ")
        )
        for team in self._teams:
            self._view._txtOutSquadre.controls.append(
                ft.Text(team)
            )

        self._fillDDTeams()
        self._view.update_page()

    def _fillDDTeams(self):
        for team in self._teams:
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(
                    data = team,
                    key = team.name,
                )
            )



    def _fillDDYears(self):
        years = self._model.getAllYears()
        for year in years:
            intYear = int(year)

            self._view._ddAnno.options.append(
                ft.dropdown.Option(
                    intYear
                )
            )