## 🛠️ Pasos para iniciar el proyecto (Backend)

### 1. Crear entorno virtual

(Solo si no existe la carpeta `venv`)

```bash
python3 -m venv venv
```

### 2. Activar el entorno virtual

```bash
source venv/bin/activate
```

### 3. Actualizar `pip` (opcional pero recomendado)

```bash
pip install --upgrade pip
```

### 4. Instalar dependencias del proyecto

```bash
pip install -r requirements.txt
```

### 5. Detener el entorno virtual

Cuando termines de trabajar, puedes salir del entorno virtual con:

```bash
deactivate
```

## Scripts

### Generar fake_orders.csv

```bash
(venv) python src/scripts/generate_fake_orders.py
```
