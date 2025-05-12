import time
import customtkinter as ctk
from customtkinter import CTkInputDialog
import threading
import keyword



activity = False
ctk.set_widget_scaling(1)
cronometros = {}
labelItem = {}
today = f"{time.localtime().tm_mday}/{time.localtime().tm_mon}/{time.localtime().tm_year}"
print(today)
opciones_short = {

}
def cut_word(word):
    return word[:8]


def desactivateCrono():
    global activity
    activity = False

def checkCronometro(name):
    if cronometros[name]["ss"] > 60:
        cronometros[name]["ss"] = 0
        cronometros[name]["mm"] += 1
    if cronometros[name]["mm"] > 60:
        cronometros[name]["mm"] = 0
        cronometros[name]["hh"] +=1 

with open("data.txt","a") as fichero:
    #fichero.write("Primeora lineaaa \n")
    pass
def find_same(date):
    with open("data.txt","r") as f:
        x = f.readlines()
        print(x)
        #while()
#find_same()

ventana = ctk.CTk()
ventana.geometry("388x312")
ventana.title("Aplicación registro de horas")
ventana.resizable(False, False) 


def AvanzarSegundos():
    if activity == True:
        cronometros[opciones_short[dropdown._current_value]]["ss"] += 1
        checkCronometro(opciones_short[dropdown._current_value])
        actualizar_corno_label()
        ventana.after(1000,AvanzarSegundos)

def actualizar_corno_label():
    reloj.configure(text = dicc_to_str(opciones_short[dropdown._current_value]))

def refresh_item_time():
    dir = labelItem[opciones_short[dropdown._current_value]]
    content = dir._text.lstrip().split(" ", 1)
    name = content[1].lstrip()
    dir.configure(text =  dicc_to_str(opciones_short[dropdown._current_value])+"  "+ name)

    pass

def total():
    seconds = 0
    for i in cronometros:
        seconds += (cronometros[i]["hh"]*3600) + (cronometros[i]['mm']*60) + cronometros[i]['ss']
    hh = seconds // 3600
    mm = (seconds % 3600) // 60
    ss = seconds % 60
    Total.configure( text = f"Total : {hh:02}:{mm:02}:{ss:02}")
def is_zero_seconds(name):
    seconds = 0
    seconds += (cronometros[name]["hh"]*3600) + (cronometros[name]['mm']*60) + cronometros[name]['ss']
    if seconds == 0:
        return True
    else:
        return False

def this_exist_already(date,name):
    with open("data.txt","r") as f:
        lines = f.readlines()
        print(lines)
        for i in reversed(lines):
            inText =  i.split("  ",2)
            if inText[0] == today:
                print()
        #open("data.txt","w").write(i)

                

def save_data():
    now = f"{time.localtime().tm_mday}/{time.localtime().tm_mon}/{time.localtime().tm_year}"
    if today == now:
        for i in cronometros:
            if not is_zero_seconds(i):

                this_exist_already(today,i)
            else:
                print(i,"no es truee")
    else:
        for i in cronometros:
            pass
            #print(f"{today}  {dicc_to_str(i)}  {i}")
            #subir lo actual y reiniciar los tiempos de los items y actualizar los labels (listas y time )



def dicc_to_str(name):
    result = ''
    for i in cronometros[name]:
        x = cronometros[name][i]
        if x < 10:
            result+= '0'+str(x)
        else:
            result+=str(x)
        result+= ':'
    return result[:-1]

def tareas_registradas(opcion):
    global activity
    if activity is True:
        pauseFunc(None)
    #Save
    print("opcion es : ",opcion)
    if opcion == "Add":
        crear_boton_con_input()
        reloj.configure(text = "00:00:00")
        return
    else:
        reloj.configure(text = dicc_to_str(opciones_short[opcion]))

# Opciones para el dropdown list
opciones = ["Add"]
ventana.grid_columnconfigure(0, weight=0)
# Crear el dropdown list (OptionMenu)
dropdown = ctk.CTkOptionMenu(ventana, values=opciones, command=tareas_registradas)
#dropdown.place( relx = 0.05, rely = 0.05)
dropdown.grid(row = 0,column = 0, pady = 15, padx = 10)
dropdown.configure(width=100,height=28)
#dropdown.pack(pady=5)
def pauseFunc(BtnMin):
    if dropdown._current_value == "Add":
        activar_animacion(dropdown)
        return
    global activity
    if activity is True:
        btnPause.configure(text = 'Start', fg_color = "green")
        activity = False 
        total()
        refresh_item_time()
        if BtnMin:
            BtnMin.configure(text = 'Start', fg_color = "green")
    elif activity is False:
        btnPause.configure(text = 'Stop',fg_color = "red")
        activity = True
        AvanzarSegundos()
        if BtnMin:
            BtnMin.configure(text = 'Stop',fg_color = "red")
    
    pass

def to_return(a):
    ventana.deiconify()
    a.destroy()
    total()
    pass


btnPause = ctk.CTkButton(ventana, text= "Start", command=lambda: pauseFunc(None),width=90,fg_color="green")
btnPause.grid(row = 0,column = 2, pady = 15, padx = 10)



def minimalistWindow():
    ventana_minimalista = ctk.CTkToplevel(ventana)
    ventana_minimalista.geometry("300x200")
    ventana_minimalista.title("Cronómetro")
    ventana_minimalista.resizable(False, False) 
    if activity is True:
        btnPauseMinimalista = ctk.CTkButton(ventana_minimalista,text="Stop",height=50,fg_color="red",command=lambda: pauseFunc(btnPauseMinimalista))
    else:
        btnPauseMinimalista = ctk.CTkButton(ventana_minimalista,text="Start",height=50,fg_color="green",command=lambda: pauseFunc(btnPauseMinimalista))
    btnPauseMinimalista.place(relx = 0.5, rely = 0.5, anchor= "center")
    
    btnReturn = ctk.CTkButton(ventana_minimalista,text = "Return",width=50,fg_color="#2e2e2e",command=lambda:to_return(ventana_minimalista))
    btnReturn.place(relx= 0.05,rely=0.1)
    ventana_minimalista.protocol("WM_DELETE_WINDOW",lambda: to_return(ventana_minimalista))
    ventana.withdraw()
    pass

btnHide = ctk.CTkButton(ventana,text="Min", command=minimalistWindow,width=60)
btnHide.grid(row = 0,column = 3, pady = 15, padx = 5)


# Crear una etiqueta que muestra la opción seleccionada
reloj = ctk.CTkLabel(ventana, text="00:00:00", font=("Arial", 16))
reloj.grid(row = 0,column = 1, pady = 15, padx = 10)
#reloj.place(relx = 0.45,rely = 0.05 )
panel_tabla = ctk.CTkFrame(ventana)
panel_tabla.grid(row=1,rowspan = 2, column=0,columnspan=5, padx=5, pady=5)
panel_tabla.grid_propagate(False)

tabla = ctk.CTkScrollableFrame(panel_tabla,width= 300,height=0)
tabla.pack(fill="both", expand=True)
#tabla.place(relx = 0.5,rely = 0.7,anchor = "center")
#tabla.grid(row=1,rowspan = 2, column=0, columnspan = 5, padx=5, pady=5 ,sticky="n")


def transform_time_str(name):
    if name in cronometros:
        result  =''
        for i in cronometros[name]:
            if cronometros[name][i] <10:
                result += '0'+str(cronometros[name][i])
            else:
                result += str(cronometros[name][i])
            result+= ':'
        return result[:-1]   
    else:
        print("No existe en crono : ",name)

def string_to_perfection(string):
    result = ''
    for i in string.split(':'):
        if int(i) < 10 :
            result += '0'+str(int(i))
        else:
            result += str(int(i))
        result +=':'
    return  result[:-1]


def transform_time_int(str):
    x = str.split(':')
    result = {'hh':int(x[0]),'mm':int(x[1]),'ss':int(x[2])}
    return result

def formato_tiempo(str):
    time = str.split(":")
    if len(time) == 3:
        if not time[0].isdigit():
            print(time[0])
            return False
        if not time[1].isdigit() or int(time[1]) >60:
            print(time[1])
            return False
        if not time[2].isdigit() or int(time[2]) >60:
            print(time[2])
            return False
        return True

def check_today():
    with open("data.txt","r") as f:
        lines = f.readlines()
        for i in reversed(lines):
            inText =  i.split("  ",2)
            if inText[0] == today:
                print(inText[2])
                #if inText[2][-2] == "\":
                name = inText[2][:-2]
                time = inText[1]
                print("datos : ",name,time)
                cronometros[name] = transform_time_int(inText[1])
                #agregar a opciones - shortoptions - cronometro y actualizar todo, y agregar a lista
                crear_boton(name,time)
            else:
                return


def refresh_opciones():
    dropdown.configure(values = opciones, width = 100)

def borrar_item(widget,ventana_dialog):
    content = widget._text.lstrip().split(" ", 1)
    name = content[1].lstrip()
    print(name)
    #labelItem.pop(name)
    widget.destroy()
    opciones.remove(cut_word(name))
    cronometros.pop(name)
    print(opciones,cronometros)
    ventana_dialog.destroy()
    refresh_opciones()
    if dropdown._current_value != 'Add' and opciones_short[dropdown._current_value] == name:
        dropdown.set('Add')
        reloj.configure(text = '00:00:00')
        desactivateCrono()
    total()

def error_animation(element):
    original_color = element.cget("fg_color")  # Guarda el color actual
    element.configure(fg_color="red")          # Cambia a rojo
    element.update()
    time.sleep(0.5)                            # Espera medio segundo
    element.configure(fg_color=original_color) # Restaura color original

def activar_animacion(widget):
    threading.Thread(target=error_animation(widget)).start()

def editActivity(widget):
    global activity
    if activity:
        pauseFunc(None)
    content = widget._text.lstrip().split(" ", 1)
    name = content[1].strip()
    print("name : ",name)
    Time = content[0].strip()
    # Crear ventana emergente (Toplevel) para las preguntas
    ventana_secundaria = ctk.CTkToplevel(ventana)
    ventana_secundaria.geometry("300x250")
    ventana_secundaria.title("Edición")
    ventana_secundaria.lift()  # Eleva la ventana
    ventana_secundaria.attributes("-topmost", True)  # La pone sobre todas las demás temporalmente
    ventana_secundaria.resizable(False, False) 

    # Pregunta 1
    label1 = ctk.CTkLabel(ventana_secundaria, text="Name : ")
    label1.pack(pady=(20,5))
    Name = ctk.StringVar(value=name)
    entrada1 = ctk.CTkEntry(ventana_secundaria, textvariable = Name)
    entrada1.pack(pady=5)
    time = ctk.StringVar(value  = Time)
    
    # Pregunta 2
    label2 = ctk.CTkLabel(ventana_secundaria, text="Time : ")
    label2.pack(pady=5)
    entrada2 = ctk.CTkEntry(ventana_secundaria, textvariable=time)
    entrada2.pack(pady=5)

    # Función para procesar las respuestas
    def procesar_respuestas():
        print(cronometros,opciones)
        tiempo = entrada2.get().strip()
        result = ""
        if tiempo != Time and formato_tiempo(tiempo):
            cronometros[name] = transform_time_int(tiempo)
            result += string_to_perfection(tiempo) +"  "
        else:   
            result += str(Time) +"  "
        new_name = entrada1.get().strip()
        if new_name != name and new_name != " ":
            cronometros[new_name] = cronometros.pop(name)
            labelItem[new_name] = labelItem.pop(name)
            index = opciones.index(cut_word(name))
            opciones[index] = cut_word(new_name)
            refresh_opciones()
            result += new_name
        else:
            result += str(name)
        print(cronometros,opciones)
        refresh_name_and_time(widget,result)
        ventana_secundaria.destroy()
    boton_borrar = ctk.CTkButton(ventana_secundaria, text="Borrar", command=lambda:borrar_item(widget,ventana_secundaria),width=75,fg_color="red")
    boton_borrar.place(relx = 0.25,rely = 0.8,anchor = "center")
    boton_procesar = ctk.CTkButton(ventana_secundaria, text="Aceptar", command=procesar_respuestas, width=75,fg_color="green")
    boton_procesar.place(relx = 0.75 , rely = 0.8, anchor = "center")
    total()

def refresh_name_and_time(widget,new_text):
    widget.configure(text=new_text)

def crear_boton_con_input():
    # Pedir al usuario un nombre para el nuevo botón
    input_usuario = CTkInputDialog(title="Nuevo Botón", text="Escribe el nombre del botón:")
    nombre_boton = input_usuario.get_input() or ""
    nombre_boton = nombre_boton.strip()
    if nombre_boton != "" and nombre_boton not in cronometros and  nombre_boton is not None:
        opciones.insert(len(opciones) - 1, cut_word(nombre_boton))
        opciones_short[cut_word(nombre_boton)] = nombre_boton
        refresh_opciones()
        nuevo_boton = ctk.CTkButton(
            tabla,
            text=f"00:00:00  {nombre_boton}",  # Texto del botón
            width=350,  # Ajustar el tamaño
            height=40,  # Ajustar la altura
            # Deshabilitar el botón para que no sea clickeable
            fg_color= "#2e2e2e",  # Usar el mismo color de fondo que la ventana
            hover_color=ventana.cget("bg"),  # Usar el mismo color al pasar el ratón
            border_width=0,  # Eliminar borde
            text_color="white",  # Color del texto (puedes cambiarlo)
            corner_radius=0, # Esquinas redondeadas
            anchor="w",
           command=lambda: editActivity(nuevo_boton)
        )
        cronometros[nombre_boton] = {"hh":0,"mm":0,"ss":0,}
        labelItem[nombre_boton] = nuevo_boton
        nuevo_boton.pack(pady=1)

def crear_boton(name,time):
    opciones.insert(len(opciones) - 1, cut_word(name))
    opciones_short[cut_word(name)] = name
    refresh_opciones()
    nuevo_boton = ctk.CTkButton(
        tabla,
        text=f"{time}  {name}",  # Texto del botón
        width=350,  # Ajustar el tamaño
        height=40,  # Ajustar la altura
        # Deshabilitar el botón para que no sea clickeable
        fg_color= "#2e2e2e",  # Usar el mismo color de fondo que la ventana
        hover_color=ventana.cget("bg"),  # Usar el mismo color al pasar el ratón
        border_width=0,  # Eliminar borde
        text_color="white",  # Color del texto (puedes cambiarlo)
        corner_radius=0, # Esquinas redondeadas
        anchor="w",
        command=lambda: editActivity(nuevo_boton)
        )
    cronometros[name] = {"hh":0,"mm":0,"ss":0,}
    labelItem[name] = nuevo_boton
    nuevo_boton.pack(pady=1)



Total = ctk.CTkLabel(ventana,text= "Total : 00:00:00")
Total.grid(column = 0,row= 3)
Total.configure(text_color="white")
#
def scale(event):
    #print(ventana.winfo_width(), ventana.winfo_height())
    pass
ventana.bind("<Configure>",scale)
ventana.focus_set()
def showAll(event):
    print("cronometros : ",cronometros)
    print("opciones : ", opciones)
    print("lableItem : ",labelItem)
    print("opciones_short : ",opciones_short)
    save_data()

check_today()
ventana.bind("q", showAll)
ventana.mainloop()
