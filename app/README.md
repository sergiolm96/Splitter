# Splitter

Splitter es una aplicación web en desarrollo para la distribución y gestión de gastos entre varios miembros. Proporciona funcionalidades similares a Tricount o Splitwise, permitiendo almacenar deudas y pagos, y optimizando el número de transacciones necesarias para equilibrar los gastos.

## Características Planeadas

- **Sistema de usuarios registrados**: Los usuarios podrán registrarse e iniciar sesión.
- **Gestión de grupos**: Los usuarios registrados podrán crear sus propios grupos dentro de la aplicación.
- **Añadir amigos**: Los usuarios podrán añadir amigos a sus grupos.
- **Gestión de deudas y pagos internos**: Los grupos podrán gestionar deudas y pagos internos de manera eficiente.

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto localmente.

### Requisitos

- Python 3.6 o superior
- pip (el gestor de paquetes de Python)
- Flask

### Paso a Paso

1. Clona el repositorio a tu máquina local:

    ```sh
    git clone https://github.com/tu-usuario/splitter.git
    cd splitter
    ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

    ```sh
    python3 -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

4. Inicializa la base de datos:

    ```sh
    python -c 'from app import init_db; init_db()'
    ```

5. Inicia la aplicación:

    ```sh
    flask run
    ```

6. Abre tu navegador y visita `http://127.0.0.1:5000/` para ver la aplicación en acción.

## Uso

### Añadir Gastos

1. En la página principal, introduce el nombre del miembro, el monto del gasto y una descripción.
2. Haz clic en "Añadir Gasto".

### Ver Transacciones

1. Haz clic en "Ver Transacciones" en la página principal.
2. Se mostrarán las transacciones necesarias para equilibrar los gastos entre los miembros.

## Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza los cambios necesarios y haz commit (`git commit -am 'Añadir nueva característica'`).
4. Empuja la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para preguntas o comentarios, puedes contactar al autor en [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com).

