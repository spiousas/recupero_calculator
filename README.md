# recupero_calculator
Web app contruida con https://streamlit.io. Para que funcione hay que instalar el streamlit (*$ pip install streamlit*) y correr en la consola *streamlit run recupero_calculator.py*.

# Archivos que se necesita para el deploy online en Heroku

(El tutorial que use esta aca: https://www.youtube.com/watch?v=skpiLtEN3yk)

Lo primero que hay que hacer es crearse un usuario en *www.heroku.com* e ir a
*devcenter.heroku.com* e instalar el CLI.

## Archivos necesarios para hacer el deploy de la app:

* **setup.sh**: Un archivo de bash que usa Heroku para autenticar.
* **Procfile**: Corre el bash y después la app en streamlit.
* **requirement.txt**: Requirements para correr la app (mejor crearlos con pipenv).

## Pasos para hacer el deploy:

1. Crear el *environment* (usando pipenv) en la carpeta donde está clonado el proyecto.
Instalar las dependencias necesarias, en este caso *streamlit*, *pandas* y *matplotlib*. Se hace corriendo *pipenv install streamlit pandas matplotlib*.

2. Crear el archivo *setup.sh* en la misma carpeta y copiar:

```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. Crear el archivo *Procfile* (con mayúscula y sin extensión) y copiar:

```bash
web: sh setup.sh && streamlit run recupero_calculator.py
```

4. Crear el *requirements.txt* haciendo *pip freeze* en el environment.

```bash
pipenv run pip freeze > requirements.txt
```

Esto crea un archivo con todas las dependencias necesarias para correr la app.

5. Logearse en Heroku con *heroku login*.

6. Crear el proyecto con (en este caso) *heroku create recuper-app*.
Y abrirla con *heroku open*. Esto nos va a dar la **url** de la app, que hasta el
momento va a estar vacía.

7. Pushear la app a Heroku con *git push heroku master*. Actualizamos la url del punto
anterior y la app ya debería estar corriendo conline.
