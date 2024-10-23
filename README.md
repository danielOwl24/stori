# Thumbnails Generator - Coding Challenge Stori
***
Este proyecto consiste en el diseño de una arquitectura de datos para un generador de miniaturas utilizando servicios en la nube. El sistema toma imágenes grandes como entrada y genera versiones más pequeñas (miniaturas) como salida.
## Descripción del proyecto
***
	1.	Recepción de imágenes: Se asume que las imágenes son proporcionadas por una fuente de datos externa (como un bucket de S3 o una API).
	2.	Generación de miniaturas: Las imágenes recibidas son procesadas para crear versiones más pequeñas utilizando una herramienta de procesamiento de imágenes.
	3.	Almacenamiento en la nube: Las miniaturas generadas son almacenadas en un bucket de destino en la nube.
	4.	Despliegue: El servicio es desplegado utilizando una herramienta de infraestructura como código (IaC), en este caso se utilizó CDK.