# API para acceder al Web Service del Banco Central

La API del Banco Central de Chile tiene como único propósito facilitar la
captura y el uso de las estadísticas que publica el Banco, poniendo a su
disposición un servicio de transmisión directo y estándar entre sistemas de
información, de datos y series obtenidos directamente de las Base de Datos
Estadísticos (BDE) que publica el Banco en su sitio web oficial.

Para hacer uso del servicio es necesario registrarse siguiendo las instrucciones
desplegadas en la página web de la
[API BDE](https://si3.bcentral.cl/estadisticas/Principal1/web_services/index.htm).
Adicionalmente, en aquel sitio se encuentra el catálogo de series disponibles a
consultar, con sus respectivos códigos de identificación.

La librería `bcchapi` contiene clases y métodos para poder hacer uso de la API
desde python. Los resultados principales de las funciones disponibles se
entregan en un objeto
[DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
de pandas, aunque también existen otras posibilidades de acuerdo a las
necesidades del usuario.


## Instalación

La librería se puede instalar desde el Python Package Index:
```
pip install bcchapi
```



## Ejemplos de uso

El objeto principal de la librería es `Siete`, que permite crear cuadros
estadísticos y buscar series disponibles. Para iniciarlo se deben incluir las
credenciales del usuario o llamar a un archivo de texto que las contenga:

```python
import bcchapi
# Incluyendo credenciales explícitamente
siete = bcchapi.Siete("usuario", "contraseña")
# O bien llamando a un archivo
siete = bcchapi.Siete(file="credenciales.txt")
```

En caso de que no conozcamos el código de la serie que se desea consultar, este
objeto permite utilizar el método `buscar` para revisar las distintas series
que de acuerdo asu nombre. El resultado es un DataFrame de pandas:

```python
# Por defecto busca en el nombre en español
siete.buscar("antofagasta")
# También se puede buscar en inglés
siete.buscar("price", ingles=True)
```

Habiendo encontrado las series que se desean consultar, el método `cuadro`
permite crear una tabla con las especificaciones requeridas por el usuario:

```python
siete.cuadro(
    series=["F032.IMC.IND.Z.Z.EP18.Z.Z.0.M", "G073.IPC.IND.2018.M"],   
    nombres=["imacec", "ipc"],
    desde="2010-01-01",
    hasta="2020-01-01",
    variacion=12, # variación 12 meses
    frecuencia="A", # frecuencia anual
    observado={"imacec":"mean", "ipc":"last"} # funciones de agregación
)
#                 imacec       ipc
#   2010-12-31       NaN       NaN
#   2011-12-31  0.062239  0.044377
#   2012-12-31  0.061553  0.014870
#   2013-12-31  0.033085  0.030144
#   2014-12-31  0.017926  0.046464
#   2015-12-31  0.021519  0.043785
#   2016-12-31  0.017530  0.027087
#   2017-12-31  0.013577  0.022696
#   2018-12-31  0.039900  0.025632
#   2019-12-31  0.007431  0.030013
#   2020-12-31 -0.006534  0.005662
```

Para extender la librería a nuevos aplicativos, dependiendo de las necesidades
del usuario, se pueden heredar las funcionalidades de la clase
`webservice.Session`. Esta clase contiene los métodos `get` y `search`, que
envuelven los métodos disponibles por el Web Service. A modo de ejemplo, si 
queremos generar una objeto que permita obtener el último dato disponible de
una serie, podemos crear la siguiente clase:

```python
class NuevaClase(bcchapi.webservice.Session):
    def ultimo_dato(self, serie:str) -> float:
        """Devuelve último dato de una serie."""
        respuesta = self.get(serie)
        valores = respuesta.Series["Obs"]
        ultimo = valores[-1]["value"]
        return float(ultimo)
```

Esta ``NuevaClase`` se inicia de manera similar a los ejemplos
presentados anteriormente:

```python
nc = NuevaClase("usuario", "contraseña")
nc.ultimo_dato("F073.TCO.PRE.Z.D") # TCO
```