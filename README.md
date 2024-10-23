# Thumbnails Generator - Coding Challenge Stori
***
Este proyecto consiste en el diseño de una arquitectura de datos para un generador de miniaturas utilizando servicios en la nube. El sistema toma imágenes grandes como entrada y genera versiones más pequeñas (miniaturas) como salida.
## Descripción del proyecto
***
1.	Recepción de imágenes: Se asume que las imágenes son proporcionadas por una fuente de datos externa (como un bucket de S3 o una API).
2.	Generación de miniaturas: Las imágenes recibidas son procesadas para crear versiones más pequeñas utilizando una herramienta de procesamiento de imágenes.
3.	Almacenamiento en la nube: Las miniaturas generadas son almacenadas en un bucket de destino en la nube.
4.	Despliegue: El servicio es desplegado utilizando una herramienta de infraestructura como código (IaC).

## Arquitectura
***
El sistema se basa en una arquitectura serverless basada en eventos utilizando los siguientes componentes:

	•	Amazon S3: Para recibir y almacenar imágenes grandes y miniaturas.
	•	Lambda Functions: Para procesar las imágenes y generar las miniaturas de manera automática cuando se suben imágenes nuevas por medio de un evento de S3.
	•	Infraestructura como código (IaC): El despliegue se realiza utilizando CDK para garantizar la consistencia y escalabilidad del sistema.