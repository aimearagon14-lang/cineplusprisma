#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import wx

# ----------------------
# Helper: sala por pelicula
# ----------------------
SALA_POR_PELI = {
    "Avatar": "Sala 1",
    "Avengers": "Sala 2",
    "Frozen": "Sala 3",
    "Mario Bros": "Sala 4",
}

# ----------------------
# VENTANA 1: Inicio de sesión
# ----------------------
class InicioSesion(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(*args, **kwds)
        self.SetSize((450, 380))
        self.SetTitle("Inicio de sesión")

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        bmp = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(1,1))  # placeholder if no image
        sizer.Add(bmp, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 10)

        # usuario
        gs1 = wx.GridSizer(1,2,0,0)
        gs1.Add(wx.StaticText(panel, label="USUARIO:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.tfUsuario = wx.TextCtrl(panel)
        gs1.Add(self.tfUsuario, 0, wx.EXPAND)
        sizer.Add(gs1, 0, wx.ALL|wx.EXPAND, 12)

        # clave
        gs2 = wx.GridSizer(1,2,0,0)
        gs2.Add(wx.StaticText(panel, label="CLAVE:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.tfClave = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        gs2.Add(self.tfClave, 0, wx.EXPAND)
        sizer.Add(gs2, 0, wx.ALL|wx.EXPAND, 12)

        # boton
        self.btnIngresar = wx.Button(panel, label="INGRESAR")
        sizer.Add(self.btnIngresar, 0, wx.ALIGN_CENTER|wx.ALL, 20)

        panel.SetSizer(sizer)
        self.Layout()

        self.btnIngresar.Bind(wx.EVT_BUTTON, self.on_ingresar)

    def on_ingresar(self, event):
        nombre = self.tfUsuario.GetValue().strip()
        clave = self.tfClave.GetValue().strip()
        if nombre == "admi" and clave == "321":
            wx.MessageBox("ACCESO AUTORIZADO", "Correcto", wx.OK | wx.ICON_INFORMATION)
            self.Hide()
            self.taquilla = Taquilla(None)
            self.taquilla.Show()
        else:
            wx.MessageBox("USUARIO O CLAVE INCORRECTOS", "Error", wx.OK | wx.ICON_ERROR)

# ----------------------
# VENTANA 2: Taquilla
# ----------------------
class Taquilla(wx.Frame):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.SetTitle("Taquilla")
        self.SetSize((450, 350))
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="TAQUILLA", style=wx.ALIGN_CENTER)
        title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(title, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)

        grid = wx.FlexGridSizer(6,2,10,10)

        grid.Add(wx.StaticText(panel, label="PELÍCULA:"))
        self.combo_pelicula = wx.ComboBox(panel, choices=list(SALA_POR_PELI.keys()), style=wx.CB_READONLY)
        grid.Add(self.combo_pelicula, 1, wx.EXPAND)

        grid.Add(wx.StaticText(panel, label="HORARIO:"))
        self.combo_horario = wx.ComboBox(panel, choices=["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"], style=wx.CB_READONLY)
        grid.Add(self.combo_horario, 1, wx.EXPAND)

        grid.Add(wx.StaticText(panel, label="BOLETOS (precios: Adulto $90, Niño $80)"))
        grid.Add((0,0))

        grid.Add(wx.StaticText(panel, label="Adultos:"))
        self.txt_adultos = wx.TextCtrl(panel, value="0", size=(50,-1))
        grid.Add(self.txt_adultos)

        grid.Add(wx.StaticText(panel, label="Niños:"))
        self.txt_ninos = wx.TextCtrl(panel, value="0", size=(50,-1))
        grid.Add(self.txt_ninos)

        main_sizer.Add(grid, 1, wx.ALL|wx.EXPAND, 15)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_retroceder = wx.Button(panel, label="RETROCEDER")
        self.btn_siguiente = wx.Button(panel, label="SIGUIENTE >>")
        button_sizer.Add(self.btn_retroceder, 0, wx.RIGHT, 40)
        button_sizer.Add(self.btn_siguiente, 0, wx.LEFT, 40)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER|wx.BOTTOM, 20)

        panel.SetSizer(main_sizer)
        self.Layout()

        # eventos
        self.btn_retroceder.Bind(wx.EVT_BUTTON, self.on_retroceder)
        self.btn_siguiente.Bind(wx.EVT_BUTTON, self.on_siguiente)

    def on_retroceder(self, event):
        # volver al inicio (mostrar frame de login de nuevo)
        self.Hide()
        self.GetParent()  # parent not used
        self.login = InicioSesion(None)
        self.login.Show()

    def on_siguiente(self, event):
        pelicula = self.combo_pelicula.GetValue()
        horario = self.combo_horario.GetValue()
        adultos = self.txt_adultos.GetValue().strip()
        ninos = self.txt_ninos.GetValue().strip()

        if pelicula == "" or horario == "":
            wx.MessageBox("Por favor selecciona película y horario.", "Faltan datos", wx.OK | wx.ICON_WARNING)
            return

        try:
            adultos = int(adultos) if adultos != "" else 0
            ninos = int(ninos) if ninos != "" else 0
            if adultos < 0 or ninos < 0:
                raise ValueError
        except:
            wx.MessageBox("Los boletos deben ser números enteros no negativos.", "Error", wx.OK | wx.ICON_ERROR)
            return

        subtotal_taquilla = adultos * 90 + ninos * 80
        sala = SALA_POR_PELI.get(pelicula, "Sala 1")

        # preparar datos para dulceria
        taq_info = {
            "pelicula": pelicula,
            "horario": horario,
            "sala": sala,
            "adultos": adultos,
            "ninos": ninos,
            "subtotal_taquilla": subtotal_taquilla
        }

        # abrir dulceria
        self.Hide()
        self.dulceria = Dulceria(None, informacion=taq_info)
        self.dulceria.Show()


# ----------------------
# VENTANA 3: Dulcería (adaptada de tu archivo)
# ----------------------
class Dulceria(wx.Frame):
    def __init__(self, parent, informacion=None, subtotal=0):
        super().__init__(parent, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSize((618, 730))
        self.SetTitle("Dulcería")
        # informacion: dict enviado desde Taquilla
        if informacion is None:
            informacion = {}
        self.taq_info = informacion

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        # --- COMBOS ---
        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "COMBOS")
        label_1.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        grid_sizer_1 = wx.GridSizer(1, 3, 0, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        # images: keep placeholders (if paths exist, they will show)
        try:
            bitmap_1 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap("/comb.png", wx.BITMAP_TYPE_ANY))
        except:
            bitmap_1 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap(1,1))
        grid_sizer_1.Add(bitmap_1, 0, wx.ALIGN_CENTER, 0)

        grid_sizer_14 = wx.GridSizer(3, 1, 0, 0)
        grid_sizer_1.Add(grid_sizer_14, 1, wx.EXPAND, 0)

        self.checkbox_1 = wx.CheckBox(self.panel_1, wx.ID_ANY, "COMBO 1")
        grid_sizer_14.Add(self.checkbox_1, 0, 0, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, "$ = 75")
        label_2.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        grid_sizer_14.Add(label_2, 0, 0, 0)

        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, "(Palomitas chicas + refresco chico)")
        grid_sizer_14.Add(label_3, 0, 0, 0)

        self.spin_ctrl_1 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_1.Add(self.spin_ctrl_1, 5, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 21)

        # --- COMBO 2 ---
        grid_sizer_3 = wx.GridSizer(1, 3, 0, 0)
        sizer_1.Add(grid_sizer_3, 1, wx.EXPAND, 0)

        try:
            bitmap_2 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap("./comnb.png", wx.BITMAP_TYPE_ANY))
        except:
            bitmap_2 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap(1,1))
        grid_sizer_3.Add(bitmap_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        grid_sizer_5 = wx.GridSizer(3, 1, 0, 0)
        grid_sizer_3.Add(grid_sizer_5, 1, wx.EXPAND, 0)

        self.checkbox_2 = wx.CheckBox(self.panel_1, wx.ID_ANY, "COMBO 2")
        grid_sizer_5.Add(self.checkbox_2, 0, 0, 0)

        label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, "$ = 130")
        label_4.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        grid_sizer_5.Add(label_4, 0, 0, 0)

        label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, "(Palomitas medianas + 2 refrescos medianos)")
        grid_sizer_5.Add(label_5, 0, 0, 0)

        self.spin_ctrl_2 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_3.Add(self.spin_ctrl_2, 5, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 21)

        # --- COMBO 3 ---
        grid_sizer_4 = wx.GridSizer(1, 3, 0, 0)
        sizer_1.Add(grid_sizer_4, 1, wx.EXPAND, 0)

        try:
            bitmap_3 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap("./grande.png", wx.BITMAP_TYPE_ANY))
        except:
            bitmap_3 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap(1,1))
        grid_sizer_4.Add(bitmap_3, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        grid_sizer_6 = wx.GridSizer(3, 1, 0, 0)
        grid_sizer_4.Add(grid_sizer_6, 1, wx.EXPAND, 0)

        self.checkbox_3 = wx.CheckBox(self.panel_1, wx.ID_ANY, "COMBO 3")
        grid_sizer_6.Add(self.checkbox_3, 0, 0, 0)

        label_6 = wx.StaticText(self.panel_1, wx.ID_ANY, "$ = 200")
        label_6.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        grid_sizer_6.Add(label_6, 0, 0, 0)

        label_7 = wx.StaticText(self.panel_1, wx.ID_ANY, "(Palomitas grandes + refrescos grandes + dulces)")
        grid_sizer_6.Add(label_7, 0, 0, 0)

        self.spin_ctrl_3 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_4.Add(self.spin_ctrl_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 21)

        # --- PALOMITAS ---
        grid_sizer_7 = wx.GridSizer(1, 3, 0, 0)
        sizer_1.Add(grid_sizer_7, 1, wx.EXPAND, 0)

        try:
            bitmap_4 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap("./palin.png", wx.BITMAP_TYPE_ANY))
        except:
            bitmap_4 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap(1,1))
        grid_sizer_7.Add(bitmap_4, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        grid_sizer_8 = wx.GridSizer(2, 1, 0, 0)
        grid_sizer_7.Add(grid_sizer_8, 1, wx.EXPAND, 0)

        label_11 = wx.StaticText(self.panel_1, wx.ID_ANY, "Palomitas")
        label_11.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        grid_sizer_8.Add(label_11, 0, 0, 0)

        label_12 = wx.StaticText(self.panel_1, wx.ID_ANY, "$ = 100")
        label_12.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        grid_sizer_8.Add(label_12, 0, 0, 0)

        grid_sizer_9 = wx.GridSizer(3, 1, 0, 0)
        grid_sizer_7.Add(grid_sizer_9, 1, wx.EXPAND, 0)

        grid_sizer_15 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_9.Add(grid_sizer_15, 1, wx.EXPAND, 0)

        self.spin_ctrl_5 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_15.Add(self.spin_ctrl_5, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        label_8 = wx.StaticText(self.panel_1, wx.ID_ANY, "Chicas")
        grid_sizer_15.Add(label_8, 0, 0, 0)

        grid_sizer_16 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_9.Add(grid_sizer_16, 1, wx.EXPAND, 0)

        self.spin_ctrl_4 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_16.Add(self.spin_ctrl_4, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        label_9 = wx.StaticText(self.panel_1, wx.ID_ANY, "Medianas")
        grid_sizer_16.Add(label_9, 0, 0, 0)

        grid_sizer_17 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_9.Add(grid_sizer_17, 1, wx.EXPAND, 0)

        self.spin_ctrl_6 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_17.Add(self.spin_ctrl_6, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        label_10 = wx.StaticText(self.panel_1, wx.ID_ANY, "Grandes")
        grid_sizer_17.Add(label_10, 0, 0, 0)

        # --- REFRESCOS ---
        grid_sizer_10 = wx.GridSizer(1, 3, 0, 0)
        sizer_1.Add(grid_sizer_10, 1, wx.EXPAND, 0)

        try:
            bitmap_5 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap("./refre.png", wx.BITMAP_TYPE_ANY))
        except:
            bitmap_5 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap(1,1))
        grid_sizer_10.Add(bitmap_5, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        grid_sizer_12 = wx.GridSizer(2, 1, 0, 0)
        grid_sizer_10.Add(grid_sizer_12, 1, wx.EXPAND, 0)

        label_13 = wx.StaticText(self.panel_1, wx.ID_ANY, "Refrescos")
        label_13.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        grid_sizer_12.Add(label_13, 0, 0, 0)

        label_14 = wx.StaticText(self.panel_1, wx.ID_ANY, "$ = 50")
        label_14.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        grid_sizer_12.Add(label_14, 0, 0, 0)

        grid_sizer_11 = wx.GridSizer(3, 1, 0, 0)
        grid_sizer_10.Add(grid_sizer_11, 1, wx.EXPAND, 0)

        grid_sizer_18 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_11.Add(grid_sizer_18, 1, wx.EXPAND, 0)

        self.spin_ctrl_7 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_18.Add(self.spin_ctrl_7, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        label_15 = wx.StaticText(self.panel_1, wx.ID_ANY, "Chico")
        grid_sizer_18.Add(label_15, 0, 0, 0)

        grid_sizer_19 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_11.Add(grid_sizer_19, 1, wx.EXPAND, 0)

        self.spin_ctrl_8 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_19.Add(self.spin_ctrl_8, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        label_16 = wx.StaticText(self.panel_1, wx.ID_ANY, "Mediano")
        grid_sizer_19.Add(label_16, 0, 0, 0)

        grid_sizer_20 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_11.Add(grid_sizer_20, 1, wx.EXPAND, 0)

        self.spin_ctrl_9 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        grid_sizer_20.Add(self.spin_ctrl_9, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        label_17 = wx.StaticText(self.panel_1, wx.ID_ANY, "Grande")
        grid_sizer_20.Add(label_17, 0, 0, 0)

        # --- SABORES ---
        grid_sizer_13 = wx.GridSizer(1, 2, 0, 0)
        sizer_1.Add(grid_sizer_13, 1, wx.EXPAND, 0)

        label_18 = wx.StaticText(self.panel_1, wx.ID_ANY, "Sabores:")
        label_18.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        grid_sizer_13.Add(label_18, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.combo_box_1 = wx.ComboBox(self.panel_1, wx.ID_ANY,
                                       choices=["fanta", "pepsi", "monster", "coca"],
                                       style=wx.CB_DROPDOWN)
        grid_sizer_13.Add(self.combo_box_1, 5, wx.ALL, 3)

        # ---- BOTONES: RETROCEDER y CONFIRMAR ----
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_retro = wx.Button(self.panel_1, label="RETROCEDER")
        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, "CONFIRMAR")
        btn_sizer.Add(self.btn_retro, 0, wx.RIGHT, 20)
        btn_sizer.Add(self.button_1, 0, wx.LEFT, 20)
        sizer_1.Add(btn_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 8)

        # Bind
        self.button_1.Bind(wx.EVT_BUTTON, self.on_confirmar)
        self.btn_retro.Bind(wx.EVT_BUTTON, self.on_retroceder)

        self.panel_1.SetSizer(sizer_1)
        self.Layout()

    def on_retroceder(self, event):
        # volver a taquilla (recrear o mostrar)
        self.Hide()
        self.taq = Taquilla(None)
        # populate with previous data if available
        info = self.taq_info
        if info:
            self.taq.combo_pelicula.SetValue(info.get("pelicula",""))
            self.taq.combo_horario.SetValue(info.get("horario",""))
            self.taq.txt_adultos.SetValue(str(info.get("adultos",0)))
            self.taq.txt_ninos.SetValue(str(info.get("ninos",0)))
        self.taq.Show()

    def on_confirmar(self, event):
        # Calcular subtotal dulcería usando precios definidos:
        precio_combo1 = 75
        precio_combo2 = 130
        precio_combo3 = 200
        precio_palomitas = 100
        precio_refresco = 50

        items = []  # lista de tuples (descripcion, cantidad, pu, subtotal)
        subtotal = 0

        # combos (solo si checkbox marcado y cantidad > 0)
        c1_q = self.spin_ctrl_1.GetValue()
        if self.checkbox_1.IsChecked() and c1_q > 0:
            s = precio_combo1 * c1_q
            items.append(( "Combo 1", c1_q, precio_combo1, s ))
            subtotal += s

        c2_q = self.spin_ctrl_2.GetValue()
        if self.checkbox_2.IsChecked() and c2_q > 0:
            s = precio_combo2 * c2_q
            items.append(( "Combo 2", c2_q, precio_combo2, s ))
            subtotal += s

        c3_q = self.spin_ctrl_3.GetValue()
        if self.checkbox_3.IsChecked() and c3_q > 0:
            s = precio_combo3 * c3_q
            items.append(( "Combo 3", c3_q, precio_combo3, s ))
            subtotal += s

        # palomitas (por tamaños)
        pal_ch = self.spin_ctrl_5.GetValue()
        if pal_ch > 0:
            s = precio_palomitas * pal_ch
            items.append(( "Palomitas (Chicas)", pal_ch, precio_palomitas, s ))
            subtotal += s

        pal_med = self.spin_ctrl_4.GetValue()
        if pal_med > 0:
            s = precio_palomitas * pal_med
            items.append(( "Palomitas (Medianas)", pal_med, precio_palomitas, s ))
            subtotal += s

        pal_gr = self.spin_ctrl_6.GetValue()
        if pal_gr > 0:
            s = precio_palomitas * pal_gr
            items.append(( "Palomitas (Grandes)", pal_gr, precio_palomitas, s ))
            subtotal += s

        # refrescos
        ref_ch = self.spin_ctrl_7.GetValue()
        if ref_ch > 0:
            s = precio_refresco * ref_ch
            items.append(( "Refresco (Chico)", ref_ch, precio_refresco, s ))
            subtotal += s

        ref_med = self.spin_ctrl_8.GetValue()
        if ref_med > 0:
            s = precio_refresco * ref_med
            items.append(( "Refresco (Mediano)", ref_med, precio_refresco, s ))
            subtotal += s

        ref_gr = self.spin_ctrl_9.GetValue()
        if ref_gr > 0:
            s = precio_refresco * ref_gr
            items.append(( "Refresco (Grande)", ref_gr, precio_refresco, s ))
            subtotal += s

        # si no hay items y tampoco combos seleccionados, confirmar seguir vacío
        if subtotal == 0 and len(items) == 0:
            dlg = wx.MessageDialog(self, "No hay productos seleccionados en dulcería.\n¿Deseas continuar con subtotal 0?", "Confirmar", wx.YES_NO | wx.ICON_QUESTION)
            res = dlg.ShowModal()
            dlg.Destroy()
            if res != wx.ID_YES:
                return

        # preparar datos para ticket: incluir taquilla info + dulceria items
        ticket_data = {
            "taquilla": self.taq_info,
            "dulceria_items": items,
            "subtotal_dulceria": subtotal
        }

        # abrir ticket
        self.Hide()
        self.ticket = Ticket(None, ticket_data)
        self.ticket.Show()


# ----------------------
# VENTANA 4: Ticket (detallado)
# ----------------------
class Ticket(wx.Frame):
    def __init__(self, *args, **kwds):
        # kwds expected: (parent, ticket_data) but we'll accept ticket_data via second arg
        parent = None
        ticket_data = {}
        if len(args) >= 2:
            parent = args[0]
            ticket_data = args[1]
        elif "ticket_data" in kwds:
            ticket_data = kwds.pop("ticket_data")

        super().__init__(parent, *(), **kwds) if parent else super().__init__(None, wx.ID_ANY)
        self.SetTitle("Ticket detallado")
        self.SetSize((400, 600))

        # When created from Dulceria we pass ticket_data as second arg; if not, check kwds
        # but in our usage we call Ticket(None, ticket_data)

        # Accept ticket_data passed via args[1] (handled above)
        self.ticket_data = ticket_data

        panel = wx.Panel(self)
        s = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="TICKET DE VENTA", style=wx.ALIGN_CENTER)
        title.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        s.Add(title, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)

        # build the detailed message
        msg_lines = []
        taq = ticket_data.get("taquilla", {})
        items = ticket_data.get("dulceria_items", [])
        sub_dul = ticket_data.get("subtotal_dulceria", 0)
        sub_taq = taq.get("subtotal_taquilla", 0)

        pelicula = taq.get("pelicula", "—")
        horario = taq.get("horario", "—")
        sala = taq.get("sala", "—")
        adultos = taq.get("adultos", 0)
        ninos = taq.get("ninos", 0)

        msg_lines.append(f"PELÍCULA: {pelicula}")
        msg_lines.append(f"HORARIO: {horario}")
        msg_lines.append(f"SALA: {sala}")
        msg_lines.append(f"ADULTOS: {adultos}")
        msg_lines.append(f"NIÑOS: {ninos}")
        msg_lines.append(f"SUBTOTAL TAQUILLA: ${sub_taq}")
        msg_lines.append("")  # blank

        msg_lines.append("DULCERÍA:")
        if items:
            for desc, qty, pu, sub in items:
                msg_lines.append(f"{desc}: {qty} x ${pu} = ${sub}")
        else:
            msg_lines.append("Sin productos")

        msg_lines.append(f"SUBTOTAL DULCERÍA: ${sub_dul}")
        msg_lines.append("")  # blank
        total = sub_taq + sub_dul
        msg_lines.append(f"TOTAL A PAGAR: ${total}")

        # Multiline read-only text ctrl to show ticket
        ticket_text = "\n".join(msg_lines)
        self.txt = wx.TextCtrl(panel, value=ticket_text, style=wx.TE_MULTILINE | wx.TE_READONLY)
        s.Add(self.txt, 1, wx.EXPAND | wx.ALL, 10)

        # botones: imprimir (simulado) y cerrar (volver al inicio)
        btns = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_imprimir = wx.Button(panel, label="IMPRIMIR (simulado)")
        self.btn_cerrar = wx.Button(panel, label="CERRAR (volver inicio)")
        btns.Add(self.btn_imprimir, 0, wx.RIGHT, 10)
        btns.Add(self.btn_cerrar, 0, wx.LEFT, 10)
        s.Add(btns, 0, wx.ALIGN_CENTER|wx.BOTTOM, 12)

        panel.SetSizer(s)
        self.Layout()

        self.btn_imprimir.Bind(wx.EVT_BUTTON, self.on_imprimir)
        self.btn_cerrar.Bind(wx.EVT_BUTTON, self.on_cerrar)

    def on_imprimir(self, event):
        # simular impresión con mensaje
        wx.MessageBox("Ticket enviado a la impresora (simulado).", "Imprimir", wx.OK | wx.ICON_INFORMATION)

    def on_cerrar(self, event):
        # cerrar todo y volver al inicio
        wx.MessageBox("Operación finalizada. Volviendo al inicio.", "Cerrar", wx.OK | wx.ICON_INFORMATION)
        self.Hide()
        inicio = InicioSesion(None)
        inicio.Show()


# ----------------------
# MAIN
# ----------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = InicioSesion(None)
    frame.Show()
    app.MainLoop()
