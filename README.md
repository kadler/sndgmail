# SNDGMAIL

## Un comando para enviar correos electrónicos desde el IBMi, usando python.

### Entorno necesario.

Para realizar este proyecto es necesario tener instaladas las herramientas open source
provistas para el IBMi, en particular este tutorila utilizarán las siguientes herramientas:

* Python 
* git
* vim
* bash
* Free RPG

Como se instalan estas extensiones, está fuera del alcance de esta serie, sin embargo,
para los interesados, la punta del ovillo se encuentra en:

[How to obtain the new Open Source for IBM i Product - 5733OPS](https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/IBM%20i%20Technology%20Updates/page/How%20to%20obtain%20the%20new%20Open%20Source%20for%20IBM%20i%20Product%20-%205733OPS)

### Agradecimientos

Quiero agradecer a Diego Kesselman de [Esselware](http://esselware.com.mx/) por poner a disposición un equipo para
el desarrollo de este proyecto.

### Parte 1-Personalizando el editor vim.

El editor vim es un editor muy potente, pero requiere de un aprendizaje.
Esta serie no cubrirá un tutorial acerca de como utilizarlo, para ello existen muchos y muy buenos
tutoriales en la red.
Si bien vim pose una curva de aprendizaje un poco dura, es muy recomendable aprenderlo, vim está presente 
en infinidad de equipos desde un router cisco ,un teléfono android, y ahora también en nuestro equipo
favorito, el IBMi.
Para aprender a utilizar vim, vim mismo incluye un tutorial al cual se accede con el comando bash:

```bash
$ vimtutor
```

Les recomiendo realizarlo, toda el cóigo de esta serie se escribirá en vim corriendo en IBMi, 
incluyendo el presente texto.

Vim es un editor muy configurable y muy extensible por medios de plugins, nuestro interes es instalar
el plugin [Syntax files for Free-Form ILE RPG ](https://github.com/andlrc/rpgle.vim)
el cual añade soporte a vim para **Free RPG**.

Para instalar los plugins en vim, hay que instalar cÃ³digo vim en el directorio donde vim almacena
sus configuraciones (sí, vim incluye su propio interprete y es posible proogramarlo para hacer 
muchas cosas).
Para simplificar la tarea de instalar un plugin, hay un plugin llamado **vundle** que es un administrador
de plugines.
Vamos a instalar vundle en nuestro vim, para ello hay que ejecutar los siguiente comandos en bash:

```bash
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

Una vez echo lo anterior, deberemos editar el archivo de configuración de vim (usando vim, por
supuesto :-) ) para agregar el siguiente código:
:
```vim
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required

Plugin 'VundleVim/Vundle.vim'
Plugin 'andlrc/rpgle.vim'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
```

Luego arrancamos vim y corremos: **:PluginsInstall**.

Con estos pasos tendremos resaltado de sintaxis cuando escribamos
el código **Free RPG** de nuestro proyecto.
 
### Parte 2-El código Python

El código Python que utilizaremos para enviar los correo está cotenido
en el archivo sndgmail.py.

El código aterior puede ejecutarse desde bash mediante:

```bash
python2 sndgmail.py "correodestino@destino.com" "correoorigen@gmail.com" "contraseña" "subject" "body" "attach"
```
En los próximos capítulos veremos como llamar a este programa desdel entorno habitual de IBMi mediante 
un comando de IBMi creado al efecto, de manera tal que podamos enviar un correo mediante gmail desde un programa RPG o CL.
**NOTA IMPORTANTE**
Para que el programa anterior funcione, es necesario habilita el acceso de aplicaciones menos seguras de gmail, para
ello les recomiendo leer el siguiente enlace [Cómo permitir que apps menos seguras accedan a tu cuenta](https://support.google.com/accounts/answer/6010255)

### Parte 3- El código Free RPG.
El código **Fre RPG** se encaga de armar la invocación a PYTHONy ejecutar el código erior.
El código rpgle puede compilarse directamente desde bash con l instrucción:

```bash
system "CRTBNDRPG PGM(QGPL/*CTLSPEC) SRCSTMF('/home/sotton/sndgmail/sndgmail.rpgle')" | view -
```

La ultima parte ** | view - ** redirige la salida (el listado de compilaci�n) hacia el utilitario
view (vim en modo readonly), el guión al final es importnte pues indica a view que lea la salida
standard para obtner los datos a mostrar.

### Parte 4-El area de datos con parámetros.

El comando almacenarála cuenta de gmail y su clave en un area de datos de manera tal que no sea
necesario ingresar estos datos cada vez que necesitemos enviar un mail.
Como medida de seguridad, se puede poner *EXCLUDE al area de datos y dar autorización adoptada
al programa RPG, si se considera necesario.

Podemos crear el area de datos directamet desde bash con :

```bash
system "DLTDTAARA QGPL/GMAILPARAM"
system "CRTDTAARA DTAARA(QGPL/GMAILPARAM) TYPE(*CHAR) LEN(300)"


system "CHGDTAARA DTAARA(GMAILPARAM (001 100)) VALUE('/home/sndgmail')             " 
system "CHGDTAARA DTAARA(GMAILPARAM (101 100)) VALUE('account@gmail.com')          " 
system "CHGDTAARA DTAARA(GMAILPARAM (201 100)) VALUE('password')                   " 
```

Los comando anteriores han sido reunidos en un pequeño script bash llamado**crtdtaara_gmailparam.sh*
, el mismo puede ejecutarse con:

```bash
source crtdtaara_gmailparam.sh 
```
El mandato bash **source** ejecuta un script de código bash.


### Parte 5-Crear el comando.

A diferencia de un programa RPG el mandato CRTCMD no permite compilar tomando un fuente
desde el IFS. por ello para compilar el comando desde nuestro proyecto sera necesario 
en primer lugar llevar nuestro fuente a un PF-SRC, esto puede realizarse directamente
desde bash mediante:

```bash
system "CPYFRMSTMF FROMSTMF\(\'/home/sndgmail/bin/sndgmai.cmd\'\) TOMBR\(\'/QSYS.LIB/QGPL.LIB/QCMDSRC.FILE/SNDGMAIL.MBR\'\) MBROPT\(*REPLACE\)"                         
system "CRTCMD CMD(QGPL/SNDGMAIL) PGM(QGPL/SNDGMAIL)  SRCFILE(QGPL/QCMDSRC) "  
```
estas instrucciones se han reunido en el script bash llamado **crtcmd_sndgmail.sh**, el mismo puede ejecutarse mediante:
```bash
source crtcmd_sndgmail.sh 
```


