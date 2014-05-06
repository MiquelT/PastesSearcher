# PastesSearcher
=========

Pastes Searcher es un script para controlar los historiales de diversas fuentes de compartición de texto o código, permitiendo la detección de strings o patrones en éstos.


Configuración
------------
El archivo de configuración por defecto estará en dentro de la carpeta "Config".

Para activar el email debemos poner un 1 al atributo "active" del tag "email".
Dentro del tag tenemos los diferentes parámetros para configurar el envío del email y los destinatarios.

El tag "proxy" sirve para utilizar la proxyList. Recomendamos utilizarla siempre o de lo contrario bloquearán el acceso de vuestra IP.
El tag "CreateProxyList" sirve para actualizar la proxyList. Es recomendable actualizarla periodicamente para no utilizar proxys desfasadas.
El tag "proxyListUpdateTime" sirve para actualizar la proxyList automáticamente cada X segundos. De esta manera nos aseguramos que las proxys están activas y funcionando.

En el tag "sitse" podemos encontrar las diferentes fuentes.
Puede activar y desactivar cualquier fuente dandole como parámetro un 1 o un 0 repectivamente.


```
<config>

     <!-- Email configuration -->
    <email active="1">
        <user>user@gmail.com</user>
        <password>password</password>
        <smtp>smtp.gmail.com:587</smtp>

         <!-- Emails to send alerts -->
        <send>destinatario1@hotmail.com</send>
        <send>destinatario2@gmail.com</send>
    </email>

    <!-- Recomended both activated (1) -->
    <proxy>1</proxy>
    <CreateProxyList>1</CreateProxyList>
    <proxyListUpdateTime>3600</proxyListUpdateTime> <!--  in seconds  -->


    <!-- config files path -->
    <regexFile>Config/regex.conf</regexFile>
    <proxysFile>Config/proxyList.conf</proxysFile>
    <resultsPath>Data/</resultsPath>

    <!-- 1 to activate the search -->
    <sites>
	<site name="pastebin">1</site>
	<site name="pastie">1</site>
	<site name="linkpaste">1</site>
	<site name="gist.github">1</site>
	<site name="ideone">1</site>
	<site name="codepad">1</site>
	<site name="snipt">1</site>
	<site name="slexy">1</site>
	<site name="dropbucket">1</site>
	<site name="paste.ru">1</site>
	<site name="paste.lisp">1</site>
	<site name="dzone">1</site>
	<site name="lpaste">1</site>
	<site name="copytaste">1</site>
    </sites>


</config>
```

ProxyList
------------
La proxyList la puede crear directamente con el programa o puede utilizar usted las proxys que quiera. Para añadir una proxy en la ProxyList debe seguir el siguiente formato:
```
IP:Port protocol
```

Donde protocol es https o http según el protocolo del proxy.

```
119.31.123.207:8000 https
46.235.92.43:80 https
212.154.154.220:8080 https
91.236.82.85:8080 http
. . .
```

Si utiliza una proxy list creada automaticamente, ésta se actualizará automaticamente. La frecuencia de actualización la puede definir en el parametro "proxyListUpdateTime". Por defecto no se actualizará más de una vez cada 15 min.

Regex
------------
El archivo regex.conf es donde pondremos los patrones de búsqueda. Puede poner simples palabras o cadenas regex.

Se buscará por cada tag "regex".
Cada regex debe tener un tag "search" y puede tener uno o más tags "include" y "exclude".

Para crear una lista de forma rápida de regex con un solo elemento a buscar, podemos crear un documento con una lista de regex, una por linea, y ejecutar el script RegexIncluder.

Para ejecutar el Script RegexIncluder deberemos indicar si queremos añadir esas regex al documento de configuración ya existente o crear un documento nuevo (-a o -n respectivamente) y a continuación indicar el path del documento que contiene la lista de regex.


```
<config>

        <!-- Example of simple search: search for "password" -->
        <regex>
                <search>password</search>
        </regex>

        <!-- Example of inclusion: search for "user" and "pass" in the same pastie -->
        <regex>
                <search>user</search>
                <include>pass</include>
        </regex>

        <!-- Example fo exclusion: search for telf" without "email" in the same pastie -->
        <regex>
                <search>telf</search>
		        <exclude>email</exclude>
        </regex>

        <!-- Example of match with an IP address with a regex string -->
        <regex>
                <search>\d+\.\d+\.\d+\.\d+</search>
        </regex>

        . . .

</config>
```


Ejecución
------------
```
python main.py [-c ConfigFilePath]
```

Dependencias
------------
* Python 2 (2.7 should be sufficient)
* [BeautifulSoup](https://pypi.python.org/pypi/BeautifulSoup/3.2.1) version 3.2.1

License
-------
Esta obra está sujeta a la licencia [Reconocimiento-NoComercial 4.0 Internacional de Creative Commons](http://creativecommons.org/licenses/by-nc/4.0/). Para ver una copia de esta licencia, visite visite[http://creativecommons.org/licenses/by-nc/4.0/](http://creativecommons.org/licenses/by-nc/4.0/).


Como puede ayudar
----------------

Si encuentra cualquier error o problema puede [contactar conmigo en Twitter](https://twitter.com/miqueltur) o por [email](mailto:miquel.tur.m@gmail.com).