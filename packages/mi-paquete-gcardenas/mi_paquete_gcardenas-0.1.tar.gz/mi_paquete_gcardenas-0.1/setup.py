from setuptools import setup, find_packages

setup(
    name="mi_paquete_gcardenas",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Aquí puedes listar las dependencias de tu paquete
    author="Tu Nombre",
    author_email="tu_email@example.com",
    description="Una breve descripción de tu paquete",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/tu_usuario/mi_paquete",  # URL de tu proyecto
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
