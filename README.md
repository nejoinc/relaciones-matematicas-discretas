# Práctica de Relaciones - Matemáticas Discretas

Aplicación con interfaz gráfica en Python para analizar relaciones y dígrafos.

## Características

La aplicación permite:

1. **Crear y mostrar una matriz de adyacencias** (de 1 y 0) que representa una relación R: A→A
2. **Mostrar la matriz de la relación inversa R⁻¹** (no la matriz inversa, sino la de R⁻¹)
3. **Determinar automáticamente las propiedades** de la relación:
   - Reflexiva / Anti-reflexiva
   - Simétrica / Anti-simétrica  
   - Transitiva
   - De Equivalencia
   - De Orden Estricto
   - De Orden Parcial
   - De Orden Total
4. **Visualizar el dígrafo** correspondiente a la relación

## Requisitos

- Python 3.7 o superior
- Dependencias (se instalan automáticamente):
  - networkx
  - matplotlib
  - numpy

## Instalación

1. Instalar las dependencias:
```bash
py -m pip install -r requirements.txt
```

## Uso

1. Ejecutar la aplicación:
```bash
py relaciones.py
```

2. En la pestaña **"Entrada de Datos"**:
   - Ingrese el conjunto A (elementos separados por comas)
     - Ejemplo: `1,2,3,4` o `a,b,c,d`
   - Ingrese los pares ordenados de la relación R
     - Formato: `(x,y)` donde x,y ∈ A
     - Ejemplo: `(1,2),(2,3),(3,1),(1,1),(2,2),(3,3)`
   - Haga clic en **"Procesar Datos"**

3. Explorar los resultados en las pestañas:
   - **Matrices**: Muestra la matriz de adyacencia de R y R⁻¹
   - **Dígrafo**: Visualiza el grafo dirigido de la relación
   - **Propiedades**: Tabla con todas las propiedades calculadas automáticamente

## Ejemplos

### Ejemplo 1: Relación de Equivalencia
- **Conjunto A**: `1,2,3`
- **Relación R**: `(1,1),(2,2),(3,3),(1,2),(2,1),(2,3),(3,2),(1,3),(3,1)`
- **Resultado**: Es reflexiva, simétrica y transitiva → **Relación de Equivalencia**

### Ejemplo 2: Orden Parcial
- **Conjunto A**: `1,2,3,4`
- **Relación R**: `(1,1),(2,2),(3,3),(4,4),(1,2),(1,3),(1,4),(2,4),(3,4)`
- **Resultado**: Es reflexiva, antisimétrica y transitiva → **Orden Parcial**

### Ejemplo 3: Orden Total
- **Conjunto A**: `1,2,3`
- **Relación R**: `(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)`
- **Resultado**: Es orden parcial y todos los elementos son comparables → **Orden Total**

## Funcionalidades Adicionales

- **Botón "Ejemplo"**: Carga un ejemplo predefinido para probar la aplicación
- **Botón "Limpiar"**: Limpia todos los datos ingresados
- **Visualización del dígrafo**: Muestra los nodos y aristas con flechas direccionales
- **Explicaciones detalladas**: Cada propiedad incluye una explicación de por qué se cumple o no

## Notas Técnicas

### Propiedades Verificadas

- **Reflexiva**: ∀a ∈ A: (a,a) ∈ R
- **Simétrica**: ∀a,b ∈ A: (a,b) ∈ R → (b,a) ∈ R
- **Transitiva**: ∀a,b,c ∈ A: (a,b) ∈ R ∧ (b,c) ∈ R → (a,c) ∈ R
- **Equivalencia**: Reflexiva + Simétrica + Transitiva
- **Orden Estricto**: Irreflexiva + Antisimétrica + Transitiva
- **Orden Parcial**: Reflexiva + Antisimétrica + Transitiva
- **Orden Total**: Orden Parcial + Comparabilidad Total

### Matriz de Relación Inversa

La matriz de la relación inversa R⁻¹ se calcula como la transpuesta de la matriz de adyacencia de R.

Si (a,b) ∈ R, entonces (b,a) ∈ R⁻¹

## Autor

Desarrollado para la práctica de Relaciones en Matemáticas Discretas.

## Licencia

Libre para uso académico.



