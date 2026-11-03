import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP Flights manager 2026"
        self._page.window_width = 1000
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None


    def load_interface(self):
        # title
        self._title = ft.Text("TdP Flights manager 2026", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW1
        self._txtInCMin = ft.TextField(label="N min compagnie")
        self._btnAnalizzaAeroporti = ft.ElevatedButton(text="Analizza Aeroporti",
                                                       on_click=self._controller.handleAnalizza)

        row1 = ft.Row([
            ft.Container(None, width=250),
            ft.Container(self._txtInCMin, width=250),
            ft.Container(self._btnAnalizzaAeroporti, width=250),
            ft.Container(None, width=250)
        ], alignment=ft.MainAxisAlignment.CENTER)

        #ROW2
        self._ddAeroportoP = ft.Dropdown(label="Aeroporto di Partenza")
        self._btnAeroportiConnessi = ft.ElevatedButton(text="Aeroporti Connessi",
                                                       on_click=self._controller.handleConnessi)
        self._ddAeroportoA = ft.Dropdown(label="Aeroporto di Destinazione")
        self._btnTestConnessione = ft.ElevatedButton(text="Test Connessione",
                                                     on_click=self._controller.handleTestConnessione)

        row2 = ft.Row([
            ft.Container(self._ddAeroportoP, width=250),
            ft.Container(self._btnAeroportiConnessi, width=150),
            ft.Container(self._ddAeroportoA, width=250),
            ft.Container(self._btnTestConnessione, width=150)
        ], alignment=ft.MainAxisAlignment.CENTER)

        #ROW3
        self._txtInNTratteMax = ft.TextField(label="Num Tratte Max")
        self._btnCercaItinerario = ft.ElevatedButton(text="Cerca Itinerario",
                                                     on_click=self._controller.handleCerca)



        row3 = ft.Row([
            ft.Container(None, width=250),
            ft.Container(self._txtInNTratteMax, width=250),
            ft.Container(self._btnCercaItinerario, width=250),
            ft.Container(None, width=250)
        ], alignment=ft.MainAxisAlignment.CENTER)

        self._txtResults = ft.ListView(expand=1,
                                       spacing=10,
                                       padding=20,
                                       auto_scroll=True)

        self._page.add(row1, row2, row3, self._txtResults)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()