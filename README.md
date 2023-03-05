Recordar crear ambiente virtual e instalar dependencias

pip install venv
python -m venv env
env/Scripts/activate
pip install -r requirements.txt

Y para correr el programa, en terminal:

uvicorn main:app --reload