import calendar
import csv
import operator
import sys
import time
import tkinter as tk
from tkinter import ttk, CENTER, messagebox
from datetime import datetime
from tkcalendar import *
from vista_semanal import *

class EtiquetaLabel(tk.Label):
    def __init__(self, master, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.current_x = 100
        self.delay = 18 # milisegundos entre actualizaciones
        self.after(self.delay, self.update)

    def update(self):
        # Obtener el ancho del widget de la etiqueta
        width = self.winfo_width()

        # Mover el texto un píxel a la izquierda
        self.current_x -= 1

        # Si el texto se ha movido completamente fuera del widget, reiniciarlo
        if self.current_x < -width:
            self.current_x = width

        # Actualizar la posición del texto en el widget
        self.place(x=self.current_x, y=0)

        # Esperar un tiempo y actualizar de nuevo
        self.after(self.delay, self.update)

class VentanaPrincipal:

    def __init__(self):
        self.ventana()

    def label_fecha(self):
        """"Metodo para fijar un reloj en tiempo real """
        dia = time.strftime("%d")
        mes = time.strftime("%m")
        year = time.strftime("%Y")
        hora = time.strftime("%H")
        minutos = time.strftime("%M")
        segundos = time.strftime("%S")
        self.label_reloj.config(text=f"{dia}/{mes}/{year} {hora}:{minutos}:{segundos}",font=("bold italic 2",15))
        self.label_reloj.after(1000, self.label_fecha)
        
    def ventana(self):
        self.root = tk.Tk()
        self.root.geometry("1080x650+100+100")
        self.root.config(background="#E59866")
        self.root.resizable(False,False)
        self.root.title("Calendario de Eventos UPATECO")

        contenedor_botones = tk.Frame(self.root,background="#E59866",highlightbackground="white",
                                      highlightthickness=2)
        contenedor_botones.place(x=0,y=-2,width=230,height=655)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.place(x=260, y=10, width=750, height=480)
        
        self.vista_general = tk.Frame(self.tabs,background="#E59866")

        self.tabs.add(self.vista_general, text="  ")



        # Calendario y sus configuraciones
        self.now = datetime.now()
        self.cal = Calendar(contenedor_botones, selectmode="day", year=self.now.year, month=self.now.month, day=self.now.day, locale="es",
                       background="white", disabledbackground="white", bordercolor="#9b9b9b",
                       headersbackground="#9b9b9b", normalbackground="white", foreground='black',
                       normalforeground='black', headersforeground='black',showweeknumbers=False,
                       showothermonthdays=False,weekendbackground = "#9b9b9b",weekendforeground="black"

                       )
        self.cal.place(x=5,y=10,width=210,height=150)


        self.buscador_button = tk.Button(contenedor_botones, text="Buscar", command=self.buscar_evento,
                                         font=("bold italic 2", 11, "bold"))
        self.buscador_button.place(x=80,y=380)
        self.buscador_button.config(fg="black")
        self.buscador_button.config(bg="#9b9b9b")

        self.buscador_input = ttk.Entry(self.root)
        self.buscador_input.place(x=45,y=420,height=27)
        tk.Label(text="Busqueda por etiquetas",background="#9b9b9b").place(x=45,y=450)

        self.vista_semanal_button = tk.Button(self.root, text="Vista Semanal", command=self.vista_semanal,
                                               font=("bold italic 2", 11, "bold"))
        self.vista_semanal_button.config(fg="black")
        self.vista_semanal_button.config(bg="#9b9b9b")
        self.vista_semanal_button.place(x=720,y=530)

        # Boton que abre una ventana para agregar un evento
        self.agregar_evento_button = tk.Button(self.root, text="Agregar Evento", command=self.evento_ventana_principal,
                                               font=("bold italic 2", 11, "bold"))
        self.agregar_evento_button.config(fg="black")
        self.agregar_evento_button.config(bg="#9b9b9b")
        self.agregar_evento_button.place(x=250,y=530)

        # Boton que abre ventana para modificar los datos de un evento. Se insertan los
        # datos automaticamente, obtenidos de lo que se haya seleccionado en el TreeView
        self.modificar_evento_button = tk.Button(self.root, text="Modificar Evento",
                                                 command=self.modificar_evento_ventana
                                                 , font=("bold italic 2", 11, "bold"))
        self.modificar_evento_button.config(fg="black")
        self.modificar_evento_button.config(bg="#9b9b9b")
        self.modificar_evento_button.place(x=400,y=530)
        # Boton que elmina un evento seleccionado del TreeView **
        self.eliminar_evento_button = tk.Button(self.root, text="Eliminar Evento", command=self.elmininar_evento
                                                , font=("bold italic 2", 11, "bold"))
        self.eliminar_evento_button.config(fg="black")
        self.eliminar_evento_button.config(bg="#9b9b9b")
        self.eliminar_evento_button.place(x=560,y=530)
        # Boton que cierra el programa ***
        self.salir_button = tk.Button(self.root, text="Salir", command=lambda: sys.exit(),
                                      font=("bold italic 2", 11, "bold"))
        self.salir_button.config(fg="black")
        self.salir_button.config(bg="#9b9b9b")
        self.salir_button.place(x=850,y=530)

        
        ttk.Label(text="Los eventos Importantes se marcan con fondo de color",background="#9b9b9b",
            font=("bold italic 2", 11)).place(x=250,y=500)


        self.tabla_treeview_general()


        self.label_reloj = ttk.Label(self.root,text=f"Bienvenido",background="#E59866",font=("bold italic 2",11))
        self.label_reloj.place(x=20, y=500, height=80)
        self.label_reloj.after(1000,self.label_fecha)



        self.root.mainloop()
    def columnas_treeview(self):
                
        # Configuraciones de la tabla (Ancho de las columnas, titulo, centrado de la vista del archivo csv)
        
        self.tabla.column("#1", width=80, anchor=CENTER)
        self.tabla.column("#2", width=130, anchor=CENTER)
        self.tabla.column("#3", width=100, anchor=CENTER)
        self.tabla.column("#4", width=45, anchor=CENTER)
        self.tabla.column("#5", width=45, anchor=CENTER)
        self.tabla.column("#6", width=95, anchor=CENTER)
        self.tabla.column("#7", width=90, anchor=CENTER)
        self.tabla.column("#8", width=70, anchor=CENTER)
        self.tabla.column("#9", width=100, anchor=CENTER)

        self.tabla["show"] = "headings"
        self.tabla.heading("#1", text="D-CREACION", anchor=CENTER)
        self.tabla.heading("#2", text="TITULO", anchor=CENTER)
        self.tabla.heading("#3", text="FECHA EVENTO", anchor=CENTER)
        self.tabla.heading("#4", text="DESDE", anchor=CENTER)
        self.tabla.heading("#5", text="HASTA", anchor=CENTER)
        self.tabla.heading("#6", text="IMPORTANCIA", anchor=CENTER)
        self.tabla.heading("#7", text="DESCRIPCION", anchor=CENTER)
        self.tabla.heading("#8", text="ETIQUETAS", anchor=CENTER)
        self.tabla.heading("#9", text="F-CREACION", anchor=CENTER)

    def tabla_treeview_general(self):
        """Tabla que muestra los datos de los eventos. Obtenidos desde el archivo agenda.csv"""
        self.tabla = ttk.Treeview(self.vista_general, height=30,
                                  columns=("#1","#2","#3","#4","#5","#6","#7","#8","#9"))
        self.tabla.place(x=0,y=0)

        self.columnas_treeview()
        # Aqui se insertan los datos del "agenda.csv" a la tabla

        with open("agenda.csv","r",newline="") as archivo_csv:
            cal = calendar.Calendar()
            now = datetime.now()
            self.mes = cal.monthdayscalendar(now.year, now.month)
            agenda = csv.DictReader(archivo_csv)
            rows = sorted(agenda, reverse=True, key=operator.itemgetter('Codigo'))
            for linea in rows:
                #Las variables obtienen los valores de las columnas. REVISAR
                agendado = linea['Agendado']
                titulo = linea['Titulo']
                fecha = linea['Fecha']
                hora_inicio = linea['Hora Inicio']
                hora_fin = linea['Hora Fin']
                importancia = linea['Importancia']
                descripcion = linea['Descripcion']
                etiquetas = linea['Etiquetas']
                codigo = linea['Codigo']

                # Si la importancia del evento es "Importante" se cambiará el color de fila. 
                # Las lines creadas con la importancia en Normal se mantienen sin modificaciones
                if importancia == "Importante":
                    self.tabla.insert('', 0, values=(agendado,titulo,fecha,hora_inicio,
                                                 hora_fin,importancia,descripcion,etiquetas,codigo),tags=("color",))
                    self.tabla.tag_configure("color",background="#F9E79F")
                else:
                    self.tabla.insert('', 0, values=(agendado, titulo, fecha, hora_inicio,
                                                     hora_fin, importancia, descripcion, etiquetas,codigo))


    def evento_ventana_principal(self):
        """Metodo que abre una ventana para ingresar los datos de un nuevo evento"""
        dia = time.strftime("%d")
        mes = time.strftime("%m")
        year = time.strftime("%Y")
        hora = time.strftime("%H")
        minutos = time.strftime("%M")
        segundos = time.strftime("%S")
        self.evento_ventana = tk.Tk()
        self.evento_ventana.geometry("254x440+190+175")
        self.evento_ventana.resizable(False, False)
        self.evento_ventana.title("Agregar Evento")
        
        # Aqui estan todos los Entry con sus respectivos Label
        ttk.Label(self.evento_ventana,text="Agregar un Nuevo Evento",font=("bold italic 2", 11, "underline"),justify="center").place(x=10,y=10)
        ttk.Label(self.evento_ventana,text="Titulo*",font=("bold italic 2",10)).place(x=10,y=40)
        self.titulo_entry = ttk.Entry(self.evento_ventana)
        self.titulo_entry.place(x=10,y=60)

        #label de fecha
        ttk.Label(self.evento_ventana,text="Fecha (dd/mm/aaaa)*",font=("bold italic 2",10)).place(x=10,y=85)
        self.fecha_entry = ttk.Entry(self.evento_ventana)
        self.fecha_entry.place(x=10,y=105)
        self.fecha_entry.insert(0,f"{dia}/{mes}/{year}")

        ttk.Label(self.evento_ventana,text="Hora Inicio*",font=("bold italic 2",10)).place(x=10,y=130)
        self.hora_entry = ttk.Entry(self.evento_ventana)
        self.hora_entry.place(x=10,y=155)
        self.hora_entry.insert(0,f"{self.now.hour}:{minutos}")

        ttk.Label(self.evento_ventana,text="Hora Finalizacion*",font=("bold italic 2",10)).place(x=10,y=180)
        self.hora_salida_entry = ttk.Entry(self.evento_ventana)
        self.hora_salida_entry.place(x=10,y=205)
        self.hora_salida_entry.insert(0,f"{self.now.hour + 1}:{minutos}")

        ttk.Label(self.evento_ventana, text="Importancia*",font=("bold italic 2",10)).place(x=10,y=230)
        self.importancia_entry = ttk.Combobox(self.evento_ventana,values=["Normal","Importante"]
                                              ,state="readonly")
        self.importancia_entry.place(x=10,y=255)

        ttk.Label(self.evento_ventana, text="Descripcion(No usar comas',')",font=("bold italic 2",10)).place(x=10,y=280)
        self.descripcion_entry = ttk.Entry(self.evento_ventana)
        self.descripcion_entry.place(x=10,y=305)

        ttk.Label(self.evento_ventana, text="Etiquetas*",font=("bold italic 2",10)).place(x=10,y=330)
        self.etiquetas_entry = ttk.Entry(self.evento_ventana)
        self.etiquetas_entry.place(x=10,y=355)

        self.cancelar_button = tk.Button(self.evento_ventana,text="Cancelar",command=lambda: self.evento_ventana.destroy())
        self.cancelar_button.place(x=20,y=400)
        self.cancelar_button.config(fg="black",font=("bold italic 2", 11, "bold"))
        self.cancelar_button.config(bg="#9b9b9b")

        self.aceptar_button = tk.Button(self.evento_ventana, text="Aceptar", command=self.enviar_datos)
        self.aceptar_button.place(x=110,y=400)
        self.aceptar_button.config(fg="black", font=("bold italic 2", 11, "bold"))
        self.aceptar_button.config(bg="#9b9b9b")

        self.evento_ventana.mainloop()

    def datos_treeview(self):
        """Metodo que toma los valores de acuerdo al elemento seleccionado en la tabla"""
        self.seleccion = self.tabla.focus()
        self.detalles = self.tabla.item(self.seleccion)
        self.valor1 = self.detalles.get("values")[0]
        self.valor2 = self.detalles.get("values")[1]
        self.valor3 = self.detalles.get("values")[2]
        self.valor4 = self.detalles.get("values")[3]
        self.valor5 = self.detalles.get("values")[4]
        self.valor6 = self.detalles.get("values")[5]
        self.valor7 = self.detalles.get("values")[6]
        self.valor8 = self.detalles.get("values")[7]
        self.valor9 = self.detalles.get("values")[8]
    def modificar_evento_ventana(self):
        """Metodo que abre una ventana para modificar los datos de un evento"""
        try:
            self.evento_ventana = tk.Tk()
            self.evento_ventana.geometry("254x440+190+175")
            self.evento_ventana.resizable(False, False)
            self.evento_ventana.title("Modificar")
            self.datos_treeview()
            # Se insertan los valores de la tabla a los Entry
            # luego poder editar los mismos y guardarlos
            ttk.Label(self.evento_ventana, text="Modificar un Evento Existente", font=("bold italic 2", 11, "underline"),
                      justify="center").place(x=10, y=10)
            ttk.Label(self.evento_ventana, text="Titulo*", font=("bold italic 2", 10)).place(x=10, y=40)
            self.titulo_entry = ttk.Entry(self.evento_ventana)
            self.titulo_entry.place(x=10, y=60)
            self.titulo_entry.insert(0,self.valor2)
            
            #Datos de Fecha a modificar

            ttk.Label(self.evento_ventana, text="Fecha (dd/mm/aaaa)*", font=("bold italic 2", 10)).place(x=10, y=85)
            self.fecha_entry = ttk.Entry(self.evento_ventana)
            self.fecha_entry.place(x=10, y=105)
            self.fecha_entry.insert(0,self.valor3)

            #Datos de Fecha a modificar

            ttk.Label(self.evento_ventana, text="Hora Inicio*", font=("bold italic 2", 10)).place(x=10, y=130)
            self.hora_entry = ttk.Entry(self.evento_ventana)
            self.hora_entry.place(x=10, y=155)
            self.hora_entry.insert(0,self.valor4)

            #Datos de Hora de Inicio a modificar

            ttk.Label(self.evento_ventana, text="Hora Finalizacion*", font=("bold italic 2", 10)).place(x=10, y=180)
            self.hora_salida_entry = ttk.Entry(self.evento_ventana)
            self.hora_salida_entry.place(x=10, y=205)
            self.hora_salida_entry.insert(0,self.valor5)

            #Datos de Hora de finalizacion a modificar

            ttk.Label(self.evento_ventana, text="Importancia*", font=("bold italic 2", 10)).place(x=10, y=230)
            self.importancia_entry = ttk.Combobox(self.evento_ventana, values=["Normal", "Importante"]
                                                  , state="readonly")
            self.importancia_entry.place(x=10, y=255)

            #Datos de Importancia a modificar

            ttk.Label(self.evento_ventana, text="Descripcion(No usar comas',')", font=("bold italic 2", 10)).place(x=10, y=280)
            self.descripcion_entry = ttk.Entry(self.evento_ventana)
            self.descripcion_entry.place(x=10, y=305)
            self.descripcion_entry.insert(0,self.valor7)

            #Datos de Descripcion a modificar

            ttk.Label(self.evento_ventana, text="Etiquetas*", font=("bold italic 2", 10)).place(x=10, y=330)
            self.etiquetas_entry = ttk.Entry(self.evento_ventana)
            self.etiquetas_entry.place(x=10, y=355)
            self.etiquetas_entry.insert(0,self.valor8)

            self.cancelar_button = tk.Button(self.evento_ventana, text="Cancelar",
                                             command=lambda: self.evento_ventana.destroy())
            self.cancelar_button.place(x=20, y=400)
            self.cancelar_button.config(fg="black", font=("bold italic 2", 11, "bold"))
            self.cancelar_button.config(bg="#9b9b9b")


            # Aqui se almacenan los valores originales que el usuario haya
            # seleccionado de la tabla. Son los valores antes de ser modificados
            self.contenido_viejo = [self.valor1, self.valor2, self.valor3, str(self.valor4),
                                    str(self.valor5), self.valor6, self.valor7, self.valor8,str(self.valor9)]

            self.aceptar_button = tk.Button(self.evento_ventana, text="Aceptar", command=self.modificar_evento)
            self.aceptar_button.place(x=110, y=400)
            self.aceptar_button.config(fg="black", font=("bold italic 2", 11, "bold"))
            self.aceptar_button.config(bg="#9b9b9b")



            self.evento_ventana.mainloop()
        except:
            # Si el usuario se olvida de seleccionar un elemento de la tabla antes de presionar
            # el boton, le mostrar este mensaje
            self.evento_ventana.destroy()
            messagebox.showerror("Aviso","Debe seleccionar un elemento de la tabla")

    
    def validacion_datos(self):
        """Metodo que utilizo para validar datos cargados en los Entry , estos mismos si no estan
           completos emitira un error de carga solicitando completar los datos"""
        return not self.titulo_entry.get() or not self.fecha_entry.get() or not self.hora_entry.get() \
            or self.importancia_entry.get() == "" or not self.hora_salida_entry.get() or not self.etiquetas_entry.get()

    def enviar_datos(self):
        """Metodo que toma los valores de los entry, y los prepara para insertarlos en el archivo csv"""
        if self.validacion_datos() == True:
            # No debe dejar campos vacios al momento de enviar los datos,
            # Salvo el de "Descripcion" que es opcional
            ttk.Label(self.evento_ventana,text="No debe dejar\ncampos vacios",foreground="red").place(x=150,y=100)
        else:
            dia = time.strftime("%d")
            mes = time.strftime("%m")
            year = time.strftime("%Y")
            # fecha = datetime.now()
            fecha_hoy = f"{dia}/{mes}/{year}"
            auxiliar = self.fecha_entry.get().split("/")
            auxiliar2 = f"{auxiliar[2]}{auxiliar[1]}{auxiliar[0]}"
            codigo = "".join(auxiliar2)
            contenido = [fecha_hoy,self.titulo_entry.get(),self.fecha_entry.get(),
                         self.hora_entry.get(),self.hora_salida_entry.get(),
                         self.importancia_entry.get(),self.descripcion_entry.get(),
                         self.etiquetas_entry.get(),str(codigo)]
            # Todos los valores son pasado por parametro al metodo
            self.agregar_evento(contenido)
            messagebox.showinfo(message="Evento agregado correctamente")
            self.evento_ventana.destroy()
            self.tabla.delete(*self.tabla.get_children())
            self.tabla_treeview_general()


    #Metodo para agregar evento
    def agregar_evento(self,contenido):
        """Metodo que inserta los valores en el archivo csv"""
        with open("agenda.csv", "a", newline="\n") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(contenido)

    #Metodo para modificar un evento
    def modificar_evento(self):
        """Metodo que modifica los datos de algun evento"""
        if self.validacion_datos() == True:
            ttk.Label(self.evento_ventana,text="No debe dejar\ncampos vacios",foreground="red").place(x=150,y=100)
        else:
            dia = time.strftime("%d")
            mes = time.strftime("%m")
            year = time.strftime("%Y") 

            fecha_hoy = f"{dia}/{mes}/{year}"
            auxiliar = self.fecha_entry.get().split("/")
            auxiliar2 = f"{auxiliar[2]}{auxiliar[1]}{auxiliar[0]}"
            codigo = "".join(auxiliar2)
            # Se guardan las modificaciones que el usuario haya hecho a los datos
            self.contenido_nuevo = [fecha_hoy, self.titulo_entry.get(), self.fecha_entry.get(),
                                    self.hora_entry.get(), self.hora_salida_entry.get(),
                                    self.importancia_entry.get(), self.descripcion_entry.get(),
                                    self.etiquetas_entry.get(),str(codigo)]
            # Lista que guardara los datos del archivo csv
            csv_nuevo = []
            # Se lee el archivo csv, luego, cuando coincida los datos seleccionados
            # se agregara la linea nueva, reemplazand a la anterior. 
            # Luego se borra el archivo csv, y se vuelve a abrir para guardar los datos
            with open("agenda.csv", "r", newline="") as archivo:
                lector = csv.reader(archivo)
                for linea in lector:
                    if linea == self.contenido_viejo: #Variable que se encuentra en el metodo "modificar_evento_ventana"
                        csv_nuevo.append(self.contenido_nuevo)
                    else:
                        csv_nuevo.append(linea)
            file = open("agenda.csv","w")
            file.close()
            with open("agenda.csv", "a", newline="") as archivo_nuevo:
                for i in csv_nuevo:
                    escritor = csv.writer(archivo_nuevo)
                    escritor.writerow(i)
            # Mensaje que emitira el boton agregar si se actualiza correctamente
            messagebox.showinfo("Aviso","Datos actualizados correctamente")
            self.evento_ventana.destroy()
            self.tabla.delete(*self.tabla.get_children())
            self.tabla_treeview_general()

    def elmininar_evento(self):
        """Metodo que elimina un evento que se haya seleccionado"""
        try:
            # Cuando encuentre la linea que quiera eliminar, borrando asi el dato deseado
            self.datos_treeview()
            contenido_viejo = [self.valor1, self.valor2, self.valor3, str(self.valor4),
                                str(self.valor5), self.valor6, self.valor7, self.valor8,str(self.valor9)]
            csv_nuevo = []
            with open("agenda.csv", "r", newline="") as archivo:
                lector = csv.reader(archivo)
                for linea in lector:
                    if linea == contenido_viejo:
                        continue
                    else:
                        csv_nuevo.append(linea)
            file = open("agenda.csv","w")
            file.close()
            with open("agenda.csv", "a", newline="") as archivo_nuevo:
                for i in csv_nuevo:
                    escritor = csv.writer(archivo_nuevo)
                    escritor.writerow(i)
            messagebox.showinfo(message="Evento eliminado correctamente")
            self.tabla.delete(*self.tabla.get_children())
            self.tabla_treeview_general()
           

        except:
            messagebox.showerror("Aviso","Debe seleccionar un elemento de la tabla")

    def buscar_evento(self):
        #Metodo para buscar por etiqueta, si coincide con los datos a buscar trae los 
        #resultados en una ventana nueva y muestra los datos 
        resultados = []
        with open("agenda.csv","r") as archivo:
            agenda = csv.DictReader(archivo)
            rows = sorted(agenda, reverse=True, key=operator.itemgetter('Codigo'))
            for evento in rows:
                etiquetas = evento['Etiquetas']
                titulo = evento["Titulo"]
                fecha = evento['Fecha']
                hora_inicio = evento['Hora Inicio']
                hora_fin = evento['Hora Fin']
                descripcion = evento["Descripcion"]
                if self.buscador_input.get() in etiquetas:
                    resultados.append(f"Evento: {titulo}\nFecha: {fecha}\nDesde: {hora_inicio} hs. Hasta: {hora_fin} hs.\nDescripcion:\n{descripcion}\n------------------  ------------------")

            label = ""
            for i in resultados:
                a = f'{i}\n'
                label = label + a
            self.ventana_buscador = tk.Tk()
            self.ventana_buscador.geometry("300x310+190+175")
            self.ventana_buscador.title("Resultados")
            self.ventana_buscador.resizable(False,False)
            area = tk.Text(self.ventana_buscador)
            area.place(x=0,y=0,width=310,height=300)
            area.insert(0.0, f"Resultados Encontrados:\n\n{label}")
            area.config(state="disabled")

            self.ventana_buscador.mainloop()
            
            
    #Funcion para redireccionar los datos a la ventana vista semanal
    
    def vista_semanal(self):
        show_week_events(datetime.today())

VentanaPrincipal()