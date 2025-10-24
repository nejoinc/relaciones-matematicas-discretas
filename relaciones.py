"""
PRÁCTICA RELACIONES - Matemáticas Discretas
Aplicación con interfaz gráfica para analizar relaciones y dígrafos
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class RelacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Relaciones y Dígrafos")
        self.root.geometry("1200x800")
        
        # Variables para almacenar datos
        self.conjunto_a = []
        self.relacion = []
        self.matriz_adyacencia = None
        self.matriz_inversa = None
        
        # Configurar interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""
        # Frame principal con notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Entrada de datos
        self.frame_entrada = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_entrada, text="Entrada de Datos")
        self.crear_frame_entrada()
        
        # Pestaña 2: Matrices
        self.frame_matrices = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_matrices, text="Matrices")
        self.crear_frame_matrices()
        
        # Pestaña 3: Dígrafo
        self.frame_digrafo = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_digrafo, text="Dígrafo")
        self.crear_frame_digrafo()
        
        # Pestaña 4: Propiedades
        self.frame_propiedades = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_propiedades, text="Propiedades")
        self.crear_frame_propiedades()
        
    def crear_frame_entrada(self):
        """Crea el frame para entrada de datos"""
        # Instrucciones
        ttk.Label(self.frame_entrada, text="INGRESO DE DATOS", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para conjunto A
        frame_conjunto = ttk.LabelFrame(self.frame_entrada, text="Conjunto A", padding=10)
        frame_conjunto.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(frame_conjunto, 
                 text="Ingrese los elementos del conjunto A separados por comas:").pack(anchor=tk.W)
        ttk.Label(frame_conjunto, 
                 text="Ejemplo: 1,2,3,4  o  a,b,c,d", 
                 font=('Arial', 9, 'italic')).pack(anchor=tk.W)
        
        self.entry_conjunto = ttk.Entry(frame_conjunto, width=50)
        self.entry_conjunto.pack(fill=tk.X, pady=5)
        
        # Frame para relación R
        frame_relacion = ttk.LabelFrame(self.frame_entrada, text="Relación R: A→A", padding=10)
        frame_relacion.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame_relacion, 
                 text="Ingrese los pares ordenados de la relación R:").pack(anchor=tk.W)
        ttk.Label(frame_relacion, 
                 text="Formato: (x,y) donde x,y ∈ A. Ejemplo: (1,2),(2,3),(3,1)", 
                 font=('Arial', 9, 'italic')).pack(anchor=tk.W)
        
        self.text_relacion = scrolledtext.ScrolledText(frame_relacion, height=8, width=60)
        self.text_relacion.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(self.frame_entrada)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="Procesar Datos", 
                  command=self.procesar_datos).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Limpiar", 
                  command=self.limpiar_datos).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Ejemplo", 
                  command=self.cargar_ejemplo).pack(side=tk.LEFT, padx=5)
        
    def crear_frame_matrices(self):
        """Crea el frame para mostrar matrices"""
        # Frame para matriz de adyacencia
        frame_adj = ttk.LabelFrame(self.frame_matrices, text="Matriz de Adyacencias de R", padding=10)
        frame_adj.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.text_matriz_adj = scrolledtext.ScrolledText(frame_adj, height=10, 
                                                         font=('Courier', 10))
        self.text_matriz_adj.pack(fill=tk.BOTH, expand=True)
        
        # Frame para matriz inversa
        frame_inv = ttk.LabelFrame(self.frame_matrices, text="Matriz de la Relación Inversa R⁻¹", padding=10)
        frame_inv.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.text_matriz_inv = scrolledtext.ScrolledText(frame_inv, height=10, 
                                                         font=('Courier', 10))
        self.text_matriz_inv.pack(fill=tk.BOTH, expand=True)
        
    def crear_frame_digrafo(self):
        """Crea el frame para mostrar el dígrafo"""
        ttk.Label(self.frame_digrafo, text="VISUALIZACIÓN DEL DÍGRAFO", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para el canvas de matplotlib
        self.frame_canvas = ttk.Frame(self.frame_digrafo)
        self.frame_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Button(self.frame_digrafo, text="Actualizar Dígrafo", 
                  command=self.dibujar_digrafo).pack(pady=5)
        
    def crear_frame_propiedades(self):
        """Crea el frame para mostrar las propiedades"""
        ttk.Label(self.frame_propiedades, text="PROPIEDADES DE LA RELACIÓN", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Tabla de propiedades
        frame_tabla = ttk.Frame(self.frame_propiedades)
        frame_tabla.pack(pady=20)
        
        # Crear tabla
        propiedades = [
            "REFLEXIVA",
            "SIMÉTRICA", 
            "TRANSITIVA",
            "DE EQUIVALENCIA",
            "DE ORDEN ESTRICTO",
            "DE ORDEN PARCIAL",
            "DE ORDEN TOTAL"
        ]
        
        # Encabezados
        ttk.Label(frame_tabla, text="PROPIEDAD", font=('Arial', 11, 'bold'), 
                 borderwidth=2, relief="solid", width=25).grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        ttk.Label(frame_tabla, text="SI", font=('Arial', 11, 'bold'), 
                 borderwidth=2, relief="solid", width=10).grid(row=0, column=1, sticky='nsew', padx=1, pady=1)
        ttk.Label(frame_tabla, text="NO", font=('Arial', 11, 'bold'), 
                 borderwidth=2, relief="solid", width=10).grid(row=0, column=2, sticky='nsew', padx=1, pady=1)
        ttk.Label(frame_tabla, text="ANTI-", font=('Arial', 11, 'bold'), 
                 borderwidth=2, relief="solid", width=10).grid(row=0, column=3, sticky='nsew', padx=1, pady=1)
        
        # Filas de propiedades
        self.labels_propiedades = {}
        for i, prop in enumerate(propiedades, start=1):
            ttk.Label(frame_tabla, text=prop, font=('Arial', 10), 
                     borderwidth=2, relief="solid", width=25).grid(row=i, column=0, sticky='nsew', padx=1, pady=1)
            
            self.labels_propiedades[prop] = {}
            for j, col in enumerate(['SI', 'NO', 'ANTI'], start=1):
                lbl = ttk.Label(frame_tabla, text="", font=('Arial', 10), 
                               borderwidth=2, relief="solid", width=10)
                lbl.grid(row=i, column=j, sticky='nsew', padx=1, pady=1)
                self.labels_propiedades[prop][col] = lbl
        
        # Frame para explicaciones
        frame_explicacion = ttk.LabelFrame(self.frame_propiedades, 
                                          text="Explicación de las Propiedades", 
                                          padding=10)
        frame_explicacion.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.text_explicacion = scrolledtext.ScrolledText(frame_explicacion, height=10, 
                                                          font=('Arial', 10))
        self.text_explicacion.pack(fill=tk.BOTH, expand=True)
        
    def procesar_datos(self):
        """Procesa los datos ingresados"""
        try:
            # Obtener conjunto A
            conjunto_str = self.entry_conjunto.get().strip()
            if not conjunto_str:
                raise ValueError("El conjunto A no puede estar vacío")
            
            self.conjunto_a = [x.strip() for x in conjunto_str.split(',')]
            n = len(self.conjunto_a)
            
            # Obtener relación R
            relacion_str = self.text_relacion.get('1.0', tk.END).strip()
            if not relacion_str:
                raise ValueError("La relación R no puede estar vacía")
            
            # Parsear pares ordenados
            self.relacion = []
            # Eliminar espacios y dividir por comas fuera de paréntesis
            import re
            pares = re.findall(r'\(([^,]+),([^)]+)\)', relacion_str)
            
            for par in pares:
                x, y = par[0].strip(), par[1].strip()
                if x not in self.conjunto_a or y not in self.conjunto_a:
                    raise ValueError(f"El par ({x},{y}) contiene elementos que no están en A")
                self.relacion.append((x, y))
            
            if not self.relacion:
                raise ValueError("No se encontraron pares ordenados válidos")
            
            # Crear matriz de adyacencia
            self.crear_matriz_adyacencia()
            
            # Crear matriz inversa
            self.crear_matriz_inversa()
            
            # Mostrar matrices
            self.mostrar_matrices()
            
            # Calcular propiedades
            self.calcular_propiedades()
            
            # Dibujar dígrafo
            self.dibujar_digrafo()
            
            messagebox.showinfo("Éxito", "Datos procesados correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar datos:\n{str(e)}")
    
    def crear_matriz_adyacencia(self):
        """Crea la matriz de adyacencia de la relación"""
        n = len(self.conjunto_a)
        self.matriz_adyacencia = np.zeros((n, n), dtype=int)
        
        for (x, y) in self.relacion:
            i = self.conjunto_a.index(x)
            j = self.conjunto_a.index(y)
            self.matriz_adyacencia[i][j] = 1
    
    def crear_matriz_inversa(self):
        """Crea la matriz de la relación inversa"""
        # La matriz inversa es la transpuesta de la matriz de adyacencia
        self.matriz_inversa = self.matriz_adyacencia.T
    
    def mostrar_matrices(self):
        """Muestra las matrices en la interfaz"""
        # Limpiar textos
        self.text_matriz_adj.delete('1.0', tk.END)
        self.text_matriz_inv.delete('1.0', tk.END)
        
        # Mostrar matriz de adyacencia
        self.text_matriz_adj.insert('1.0', self.formatear_matriz(self.matriz_adyacencia, "R"))
        
        # Mostrar matriz inversa
        self.text_matriz_inv.insert('1.0', self.formatear_matriz(self.matriz_inversa, "R⁻¹"))
    
    def formatear_matriz(self, matriz, nombre):
        """Formatea una matriz para mostrarla"""
        resultado = f"Matriz de adyacencia de {nombre}:\n\n"
        
        # Encabezado de columnas
        resultado += "     " + "  ".join(f"{elem:>3}" for elem in self.conjunto_a) + "\n"
        resultado += "   " + "-" * (4 * len(self.conjunto_a) + 2) + "\n"
        
        # Filas
        for i, elem in enumerate(self.conjunto_a):
            resultado += f"{elem:>3} |"
            for j in range(len(self.conjunto_a)):
                resultado += f" {matriz[i][j]:>3}"
            resultado += "\n"
        
        # Mostrar pares ordenados
        pares = []
        for i in range(len(self.conjunto_a)):
            for j in range(len(self.conjunto_a)):
                if matriz[i][j] == 1:
                    pares.append(f"({self.conjunto_a[i]},{self.conjunto_a[j]})")
        
        resultado += f"\n{nombre} = {{{', '.join(pares)}}}\n"
        
        return resultado
    
    def dibujar_digrafo(self):
        """Dibuja el dígrafo de la relación"""
        if self.matriz_adyacencia is None:
            messagebox.showwarning("Advertencia", "Primero debe procesar los datos")
            return
        
        # Limpiar frame anterior
        for widget in self.frame_canvas.winfo_children():
            widget.destroy()
        
        # Crear figura de matplotlib
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Crear grafo dirigido
        G = nx.DiGraph()
        
        # Agregar nodos
        G.add_nodes_from(self.conjunto_a)
        
        # Agregar aristas
        for (x, y) in self.relacion:
            G.add_edge(x, y)
        
        # Dibujar grafo
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', 
                              node_size=800, alpha=0.9)
        
        # Dibujar etiquetas de nodos
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold')
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', 
                              arrows=True, arrowsize=20, arrowstyle='->', 
                              connectionstyle='arc3,rad=0.1', width=2)
        
        ax.set_title(f"Dígrafo de la Relación R", fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def calcular_propiedades(self):
        """Calcula las propiedades de la relación"""
        # Limpiar tabla
        for prop in self.labels_propiedades:
            for col in ['SI', 'NO', 'ANTI']:
                self.labels_propiedades[prop][col].config(text="", background='white')
        
        explicaciones = []
        
        # Verificar reflexividad e irreflexividad
        es_reflexiva = self.es_reflexiva()
        es_irreflexiva = self.es_irreflexiva()
        
        if es_irreflexiva:
            self.marcar_propiedad("REFLEXIVA", "ANTI")
            explicaciones.append("ANTI-REFLEXIVA: SÍ - Ningún elemento tiene lazo (a,a)")
        elif es_reflexiva:
            self.marcar_propiedad("REFLEXIVA", "SI")
            explicaciones.append("REFLEXIVA: SÍ - Todos los elementos tienen lazo (a,a)")
        else:
            self.marcar_propiedad("REFLEXIVA", "NO")
            explicaciones.append("REFLEXIVA: NO - No todos los elementos tienen lazo")
        
        # Verificar simetría y antisimetría
        es_simetrica = self.es_simetrica()
        es_antisimetrica = self.es_antisimetrica()
        
        if es_antisimetrica:
            self.marcar_propiedad("SIMÉTRICA", "ANTI")
            explicaciones.append("ANTI-SIMÉTRICA: SÍ - Si (a,b) y (b,a) entonces a=b")
        elif es_simetrica:
            self.marcar_propiedad("SIMÉTRICA", "SI")
            explicaciones.append("SIMÉTRICA: SÍ - Para todo (a,b), existe (b,a)")
        else:
            self.marcar_propiedad("SIMÉTRICA", "NO")
            explicaciones.append("SIMÉTRICA: NO - Existe (a,b) sin su (b,a)")
        
        # Verificar transitividad
        es_transitiva = self.es_transitiva()
        self.marcar_propiedad("TRANSITIVA", "SI" if es_transitiva else "NO")
        explicaciones.append(f"TRANSITIVA: {'SÍ' if es_transitiva else 'NO'} - " +
                           ("Si (a,b) y (b,c) entonces existe (a,c)" if es_transitiva 
                            else "Existe (a,b) y (b,c) sin (a,c)"))
        
        # Verificar equivalencia (reflexiva + simétrica + transitiva)
        es_equivalencia = es_reflexiva and es_simetrica and es_transitiva
        self.marcar_propiedad("DE EQUIVALENCIA", "SI" if es_equivalencia else "NO")
        explicaciones.append(f"DE EQUIVALENCIA: {'SÍ' if es_equivalencia else 'NO'} - " +
                           ("Es reflexiva, simétrica y transitiva" if es_equivalencia 
                            else "No cumple todas las condiciones"))
        
        # Verificar orden estricto (irreflexiva + antisimétrica + transitiva)
        # IMPORTANTE: Orden estricto y orden parcial son MUTUAMENTE EXCLUYENTES
        es_orden_estricto = es_irreflexiva and es_antisimetrica and es_transitiva
        self.marcar_propiedad("DE ORDEN ESTRICTO", "SI" if es_orden_estricto else "NO")
        explicaciones.append(f"DE ORDEN ESTRICTO: {'SÍ' if es_orden_estricto else 'NO'} - " +
                           ("Es irreflexiva, antisimétrica y transitiva" if es_orden_estricto 
                            else "No cumple todas las condiciones"))
        
        # Verificar orden parcial (reflexiva + antisimétrica + transitiva)
        # Si es orden estricto (irreflexiva), NO puede ser orden parcial (reflexiva)
        es_orden_parcial = es_reflexiva and es_antisimetrica and es_transitiva and not es_orden_estricto
        self.marcar_propiedad("DE ORDEN PARCIAL", "SI" if es_orden_parcial else "NO")
        if es_orden_estricto:
            explicaciones.append("DE ORDEN PARCIAL: NO - Es orden estricto (mutuamente excluyente)")
        else:
            explicaciones.append(f"DE ORDEN PARCIAL: {'SÍ' if es_orden_parcial else 'NO'} - " +
                               ("Es reflexiva, antisimétrica y transitiva" if es_orden_parcial 
                                else "No cumple todas las condiciones"))
        
        # Verificar orden total (orden parcial + comparabilidad total)
        # Si es orden estricto, tampoco puede ser orden total
        es_orden_total = es_orden_parcial and self.es_total() and not es_orden_estricto
        self.marcar_propiedad("DE ORDEN TOTAL", "SI" if es_orden_total else "NO")
        if es_orden_estricto:
            explicaciones.append("DE ORDEN TOTAL: NO - Es orden estricto (mutuamente excluyente)")
        else:
            explicaciones.append(f"DE ORDEN TOTAL: {'SÍ' if es_orden_total else 'NO'} - " +
                               ("Es orden parcial y cualquier par es comparable" if es_orden_total 
                                else "No es orden parcial o faltan comparaciones"))
        
        # Mostrar explicaciones
        self.text_explicacion.delete('1.0', tk.END)
        self.text_explicacion.insert('1.0', '\n\n'.join(explicaciones))
    
    def marcar_propiedad(self, propiedad, columna):
        """Marca una propiedad en la tabla"""
        self.labels_propiedades[propiedad][columna].config(text="X", background='lightgreen')
    
    def es_reflexiva(self):
        """Verifica si la relación es reflexiva"""
        for i in range(len(self.conjunto_a)):
            if self.matriz_adyacencia[i][i] != 1:
                return False
        return True
    
    def es_irreflexiva(self):
        """Verifica si la relación es irreflexiva"""
        for i in range(len(self.conjunto_a)):
            if self.matriz_adyacencia[i][i] == 1:
                return False
        return True
    
    def es_simetrica(self):
        """Verifica si la relación es simétrica"""
        n = len(self.conjunto_a)
        for i in range(n):
            for j in range(n):
                if self.matriz_adyacencia[i][j] != self.matriz_adyacencia[j][i]:
                    return False
        return True
    
    def es_antisimetrica(self):
        """Verifica si la relación es antisimétrica"""
        n = len(self.conjunto_a)
        for i in range(n):
            for j in range(n):
                if i != j and self.matriz_adyacencia[i][j] == 1 and self.matriz_adyacencia[j][i] == 1:
                    return False
        return True
    
    def es_transitiva(self):
        """Verifica si la relación es transitiva"""
        n = len(self.conjunto_a)
        for i in range(n):
            for j in range(n):
                if self.matriz_adyacencia[i][j] == 1:
                    for k in range(n):
                        if self.matriz_adyacencia[j][k] == 1:
                            if self.matriz_adyacencia[i][k] != 1:
                                return False
        return True
    
    def es_total(self):
        """Verifica si todo par de elementos es comparable"""
        n = len(self.conjunto_a)
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Debe existir (i,j) o (j,i)
                    if self.matriz_adyacencia[i][j] != 1 and self.matriz_adyacencia[j][i] != 1:
                        return False
        return True
    
    def limpiar_datos(self):
        """Limpia todos los datos ingresados"""
        self.entry_conjunto.delete(0, tk.END)
        self.text_relacion.delete('1.0', tk.END)
        self.text_matriz_adj.delete('1.0', tk.END)
        self.text_matriz_inv.delete('1.0', tk.END)
        self.text_explicacion.delete('1.0', tk.END)
        
        # Limpiar tabla de propiedades
        for prop in self.labels_propiedades:
            for col in ['SI', 'NO', 'ANTI']:
                self.labels_propiedades[prop][col].config(text="", background='white')
        
        # Limpiar dígrafo
        for widget in self.frame_canvas.winfo_children():
            widget.destroy()
        
        self.conjunto_a = []
        self.relacion = []
        self.matriz_adyacencia = None
        self.matriz_inversa = None
    
    def cargar_ejemplo(self):
        """Carga un ejemplo predefinido"""
        self.entry_conjunto.delete(0, tk.END)
        self.entry_conjunto.insert(0, "1,2,3,4")
        
        self.text_relacion.delete('1.0', tk.END)
        self.text_relacion.insert('1.0', "(1,1),(1,2),(2,2),(2,3),(3,3),(3,1),(4,4)")


def main():
    """Función principal"""
    root = tk.Tk()
    app = RelacionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
