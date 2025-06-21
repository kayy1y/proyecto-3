import tkinter as tk
from tkinter import messagebox, filedialog
import pygame
import sys
from codificador import codificar_archivo
from decodificador import decodificar_archivo
from decodificador import leer_archivo_binario, construir_arbol, bytes_a_bits, decodificar_bits
from arbol import animar_construccion
from visualizador_pygame import animar_construccion_y_decodificacion
from codificador import obtener_ultima_ruta_bin

# === Ventana principal con opciones ===
def iniciar_tkinter():
    root = tk.Tk()
    root.title("Decodificador Gráfico de Mensajes")
    root.geometry("500x400")

    titulo = tk.Label(root, text="Decodificador Gráfico de Mensajes", font=("Arial", 16))
    titulo.pack(pady=20)

    btn_codificar = tk.Button(root, text="Codificar mensaje", width=30, command=ventana_codificar)
    btn_codificar.pack(pady=10)

    btn_visualizar_arbol = tk.Button(root, text="Visualizar árbol desde mensaje", width=30, command=ventana_visualizar_arbol)
    btn_visualizar_arbol.pack(pady=10)

    btn_paso_a_paso = tk.Button(root, text="Mostrar árbol y paso a paso", width=30, command=ventana_paso_a_paso)
    btn_paso_a_paso.pack(pady=10)

    btn_decodificar = tk.Button(root, text="Decodificar archivo .bin", width=30, command=ventana_decodificar)
    btn_decodificar.pack(pady=10)

    btn_salir = tk.Button(root, text="Salir", width=30, command=root.quit)
    btn_salir.pack(pady=10)

    root.mainloop()

# === Codificación ===
def ventana_codificar():
    def ejecutar():
        mensaje = entrada.get("1.0", tk.END).strip()
        if not mensaje:
            messagebox.showwarning("Advertencia", "Debe ingresar un mensaje.")
            return
        try:
            from collections import Counter
            from codificador import construir_arbol_con_animacion, generar_tabla_codigos, codificar_mensaje, bits_a_bytes, escribir_archivo_bin
            frecuencias = dict(Counter(mensaje))
            arbol, pasos = construir_arbol_con_animacion(frecuencias)
            tabla = generar_tabla_codigos(arbol)
            bits = codificar_mensaje(mensaje, tabla)
            bytes_codificados, bits_descartados = bits_a_bytes(bits)
            ruta_completa = codificar_archivo(mensaje)

            info = f"Frecuencias: {frecuencias}\nTabla de códigos: {tabla}\nBits codificados: {bits}\nBits descartados: {bits_descartados}\nArchivo guardado en: salida.bin"
            resultado.config(state="normal")
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END, info)
            resultado.config(state="disabled")

            messagebox.showinfo("Éxito", "Mensaje codificado y guardado como salida.bin")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    ventana = tk.Toplevel()
    ventana.title("Codificar Mensaje")
    ventana.geometry("550x400")

    label = tk.Label(ventana, text="Ingrese el mensaje a codificar:")
    label.pack(pady=10)

    entrada = tk.Text(ventana, height=5, width=60)
    entrada.pack(pady=10)

    boton = tk.Button(ventana, text="Codificar", command=ejecutar)
    boton.pack(pady=10)

    resultado = tk.Text(ventana, height=10, width=65, state="disabled")
    resultado.pack(pady=10)

# === Visualizar árbol sin guardar archivo ===
def ventana_visualizar_arbol():
    def ejecutar():
        from collections import Counter
        from codificador import construir_arbol_con_animacion
        mensaje = entrada.get("1.0", tk.END).strip()
        if not mensaje:
            messagebox.showwarning("Advertencia", "Debe ingresar un mensaje.")
            return
        frecuencias = dict(Counter(mensaje))
        arbol, pasos = construir_arbol_con_animacion(frecuencias)
        animar_construccion(pasos)

    ventana = tk.Toplevel()
    ventana.title("Visualizar Árbol de Huffman")
    ventana.geometry("400x250")

    label = tk.Label(ventana, text="Ingrese el mensaje para generar el árbol:")
    label.pack(pady=10)

    entrada = tk.Text(ventana, height=5, width=40)
    entrada.pack(pady=10)

    boton = tk.Button(ventana, text="Visualizar Árbol", command=ejecutar)
    boton.pack(pady=10)

# === Decodificación ===
def ventana_decodificar():
    archivo = filedialog.askopenfilename(
    title="Seleccione el archivo binario",
    initialdir="binarios",
    filetypes=[("Archivos binarios", "*.bin")]
    )

    if not archivo:
        return

    try:
        frecuencias, bits_descartados, codificados = leer_archivo_binario(archivo)
        arbol = construir_arbol(frecuencias)
        bits = bytes_a_bits(codificados, bits_descartados)
        animar_construccion_y_decodificacion(frecuencias, bits,arbol)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al decodificar el archivo: {e}")

# === Paso a paso ===
def ventana_paso_a_paso():
    archivo = filedialog.askopenfilename(
        title="Seleccione el archivo binario", 
        filetypes=[("Archivos binarios", "*.bin")]
    )
    if not archivo:
        return

    try:
        # ← Esta línea debe devolver una lista de tuplas [('a', 2), ...]
        frecuencias_lista, bits_descartados, codificados = leer_archivo_binario(archivo)
        
        # ← Construimos el árbol con la lista
        arbol = construir_arbol(frecuencias_lista)
        bits = bytes_a_bits(codificados, bits_descartados)

        # ← Transformamos la lista en diccionario solo para la animación
        frecuencias_dict = dict(frecuencias_lista)

        # ← Usamos el orden correcto de argumentos
        animar_construccion_y_decodificacion(frecuencias_dict, bits, arbol)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al mostrar paso a paso: {e}")


if __name__ == "__main__":
    iniciar_tkinter()
