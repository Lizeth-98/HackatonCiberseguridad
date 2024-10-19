# `HackatonITA`
El proyecto se enfoca en resguardar la seguridad mediante el uso de drones capaces de recorrer más de 30 km., ofreciendo así una solución de monitoreo en tiempo real para combatir la actividad delictiva con optimización de rutas  mediante mapeo de las zonas a patrullar. Utiliza drones equipados con cámaras  y un sistema de visión para el reconocimiento facial. Además de brindar un análisis delictivo basado en inteligencia artificial, que analiza los datos captados por los drones y los almacena de forma descentralizada utilizando tecnología de ICP (Internet Computer Protocol) para mayor seguridad y confidencialidad.

Para aprender sobre `HackatonITA`, mira la informacion que esta disponible en linea:

- [Quick Start](https://internetcomputer.org/docs/current/developer-docs/setup/deploy-locally)
- [SDK Developer Tools](https://internetcomputer.org/docs/current/developer-docs/setup/install)

If you want to start working on your project right away, you might want to try the following commands:

```bash
git clone 
cd HackatonITA/
dfx help
dfx canister --help
```
## Preparacion del entorno
Para empezar a preparar el proyecto para su funcionamiento tendremos que instalar vaarias dependencias y paquetes para su correcto funcionamiento, empezaremos con todo el tema de python para usar kybra, puedes copiar todas las lineas y correrlo en la terminal sin problemas
```bash
sudo apt-get update && sudo apt-get install make build-essential libssl-dev \
    zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
curl https://pyenv.run | bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
source ~/.bashrc
pyenv install 3.10.7
pyenv shell 3.10.7
pyenv local 3.10.7
pyenv global 3.10.7
pip install kybra
```

Una vez instalado todo esto, faltaran 2 dependencias importantes las cuales se instalaran con las siguientes lineas:
```bash
npm install react-router-dom
npm i --save @dfinity/auth-client
```
Nos serviran para el uso de internet identity y comunicar las paginas del proyecto

### Arrancar el proyecto
Una vez teniendo el proyecto y todo lo anterior instalado, procederemos con los pasos para correr el proyecto.

```bash
#Para inicializar dfx sin que capture la terminal
dfx start --background 
#Para correr el proyecto una vez inicializado
dfx deploy
```
Apareceran varios enlaces en la terminal, de estos el que nos interesa entrar es el del frontend, aparecera algo asi: " http://127.0.0.1:4943/?canisterId=bd3sg-teaaa-aaaaa-qaaba-cai"
En este usamos internet identity para iniciar sesion y una vez iniciada la sesion se desplegara un menu con 3 opciones, "Zona" que sera donde podamos buscar los crimenes por zona, "Crimen" para buscar por crimen y muestre las zonas donde han sucedido y "Reportar" que sera en donde nosotros si detectamos un comportamiento sospechoso de parte de alguien o un crimen como tal, se pueda generar un registro de la zona y el crimen que esta sucediendo.