import tkinter as tk
from tkinter import messagebox
from collections import deque

# Clase para representar un proceso
class Proceso:
    def __init__(self, id, llegada, duracion, prioridad=0):
        self.id = id
        self.llegada = llegada
        self.duracion = duracion
        self.restante = duracion  # Tiempo restante para completar el proceso
        self.prioridad = prioridad

# Función FIFO
def FIFO(procesos):
    procesos_ordenados = sorted(procesos, key=lambda p: p.llegada)
    tiempo = 0
    resultados = []
    for p in procesos_ordenados:
        tiempo_espera = max(0, tiempo - p.llegada)
        tiempo += p.duracion
        resultados.append(f"Proceso {p.id}: Inicio: {p.llegada}, Fin: {tiempo}, Espera: {tiempo_espera}")
    return resultados

# Función Prioritario
def Prioritario(procesos):
    procesos_ordenados = sorted(procesos, key=lambda p: (p.prioridad, p.llegada))
    tiempo = 0
    resultados = []
    for p in procesos_ordenados:
        tiempo_espera = max(0, tiempo - p.llegada)
        tiempo += p.duracion
        resultados.append(f"Proceso {p.id}: Inicio: {p.llegada}, Fin: {tiempo}, Espera: {tiempo_espera}")
    return resultados

# Función Round Robin
def RoundRobin(procesos, quantum=2):
    queue = deque(procesos)
    tiempo = 0
    resultados = []
    while queue:
        p = queue.popleft()
        if p.restante > quantum:
            p.restante -= quantum
            tiempo += quantum
            queue.append(p)
            resultados.append(f"Proceso {p.id}: Ejecutado durante {quantum} unidades, Tiempo actual: {tiempo}")
        else:
            tiempo += p.restante
            resultados.append(f"Proceso {p.id}: Ejecutado durante {p.restante} unidades, Tiempo actual: {tiempo}")
            p.restante = 0
    return resultados

# Función para ejecutar la simulación y mostrar resultados
def ejecutar_simulacion():
    try:
        # Obtener los valores de los inputs
        cantidad_procesos = int(entry_cantidad.get())
        procesos = []
        
        for i in range(cantidad_procesos):
            llegada = int(entry_llegada.get())
            duracion = int(entry_duracion.get())
            prioridad = int(entry_prioridad.get()) if entry_prioridad.get() else 0
            proceso = Proceso(i+1, llegada, duracion, prioridad)
            procesos.append(proceso)
        
        # Elegir el algoritmo
        algoritmo = combobox_algoritmo.get()
        if algoritmo == "FIFO":
            resultados = FIFO(procesos)
        elif algoritmo == "Prioritario":
            resultados = Prioritario(procesos)
        elif algoritmo == "Round Robin":
            resultados = RoundRobin(procesos)
        else:
            messagebox.showerror("Error", "Algoritmo no seleccionado")
            return
        
        # Mostrar resultados en el área de texto
        resultados_text.delete(1.0, tk.END)
        for resultado in resultados:
            resultados_text.insert(tk.END, resultado + "\n")
    
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores válidos para los procesos.")

# Crear la ventana principal
root = tk.Tk()
root.title("Simulación de Algoritmos de Planificación")

# Crear los campos de entrada
tk.Label(root, text="Cantidad de Procesos:").grid(row=0, column=0)
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=0, column=1)

tk.Label(root, text="Tiempo de Llegada:").grid(row=1, column=0)
entry_llegada = tk.Entry(root)
entry_llegada.grid(row=1, column=1)

tk.Label(root, text="Duración del Proceso:").grid(row=2, column=0)
entry_duracion = tk.Entry(root)
entry_duracion.grid(row=2, column=1)

tk.Label(root, text="Prioridad (opcional):").grid(row=3, column=0)
entry_prioridad = tk.Entry(root)
entry_prioridad.grid(row=3, column=1)

# Crear el combo box para seleccionar el algoritmo
tk.Label(root, text="Seleccione el Algoritmo:").grid(row=4, column=0)
combobox_algoritmo = tk.StringVar()
combobox = tk.OptionMenu(root, combobox_algoritmo, "FIFO", "Prioritario", "Round Robin")
combobox.grid(row=4, column=1)

# Crear botón para ejecutar la simulación
btn_ejecutar = tk.Button(root, text="Ejecutar Simulación", command=ejecutar_simulacion)
btn_ejecutar.grid(row=5, column=0, columnspan=2)

# Crear el área de texto para mostrar los resultados
resultados_text = tk.Text(root, width=50, height=10)
resultados_text.grid(row=6, column=0, columnspan=2)

# Ejecutar la aplicación
root.mainloop()
