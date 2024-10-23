# Thumbnails Generator - Coding Challenge Stori
***
Este proyecto consiste en el diseño de una arquitectura de datos para un generador de miniaturas utilizando servicios en la nube. El sistema toma imágenes grandes como entrada y genera versiones más pequeñas (miniaturas) como salida.
## Descripción del proyecto
***
1. **Recepción de imágenes**: Se asume que las imágenes son proporcionadas por una fuente de datos externa (como un bucket de S3 o una API).
2. **Generación de miniaturas**: Las imágenes recibidas son procesadas para crear versiones más pequeñas utilizando una herramienta de procesamiento de imágenes.
3. **Almacenamiento en la nube**: Las miniaturas generadas son almacenadas en un bucket de destino en AWS.
4. **Despliegue**: La insfraestructura es desplegada utilizando una herramienta de infraestructura como código (IaC).

## Arquitectura
***
El sistema se basa en una arquitectura **serverless** basada en eventos utilizando los siguientes componentes:

- **Amazon S3**: Para recibir y almacenar imágenes grandes y miniaturas.
- **Lambda Functions**: Para procesar las imágenes y generar las miniaturas de manera automática cuando se suben imágenes nuevas por medio de un evento de S3. Se agregó esta función a una VPC y una subnet sin acceso a internet por lo que para acceder a los buckets de S3 y la tabla de DynamoDB es necesario configurar un VPC endpoint.
- **Infraestructura como código (IaC)**: El despliegue se realiza utilizando CDK para garantizar la consistencia y escalabilidad del sistema.

<p align="center">
  <img src="images/arquitectura_thumbnails.drawio.png" alt="Arquitectura propuesta para la solución" width="400"/>
</p>

## Herramientas y Tecnologías
***
- **Python**: Para escribir el código del generador de miniaturas.
- **Pillow**: Librería de Python utilizada para procesar imágenes.
- **Amazon Web Services (AWS)**: Servicios utilizados incluyen S3, Lambda y CDK para el despliegue. 

## Instalación y Despliegue

Sigue estos pasos para desplegar el servicio:

1.	Clona el repositorio:
    ```git clone https://github.com/danielOwl24/stori.git```
    ```cd stori```
2. Instalar Node.js
3. Verificar instalación de Node.js
    ```node -v```
    ```npm -v```
3. Instalar AWS CDK
    ```npm install -g aws-cdk```
4. Verificar instalación de AWS CDK
    ```cdk --version```
5. Crea un entorno virtual para instalar las dependencias, esto puede variar de un sistema operativo a otro, para este caso se desarrolló en macOS.
   ```python3 -m venv $environment_name$```
6. Activa el entorno virtual.
    ```source environment_name/bin/activate```
7. Instala las dependecias del proyecto.
    ```pip install -r requirements.txt```
8. Configura las credenciales de AWS. Es necesario tener instalado AWS CLI.
    ```aws config```
9. Configura las variables de entorno como la cuenta de AWS, la región, etc; las cuales son necesarias para la ejecución de la aplicación. La forma de crear estas variables de entorno depende del sistema operativo.
10. Ejecutar el comando bootstrap para desplegar la aplicación por primera vez y arrancar el proyecto con las configuraciones de AWS ingresadas anteriormente.
    ```cdk bootstrap```
11. Lista los stacks del CDK actual.
    ```cdk list```
12. Ejecuta el siguiente comando para que CloudFormation lleve a cabo una validación previa del código del stack antes del despliegue.
    ```cdk synth```
13. Desplegar la infraestructura configurada en la aplicación de CDK por medio de CloudFormation en la cuenta de AWS.
   ```cdk deploy```
14. Validar que los servicios se hayan desplegado correctamente en AWS.

## Explicación del Proyecto

Este proyecto utiliza una arquitectura basada en eventos y disponible para ser desplegada en una cuenta de AWS, donde cada vez que una imagen es subida al bucket S3 de origen, un evento de S3 activa una función Lambda que genera la miniatura correspondiente y la guarda en un bucket de destino.

### Supuestos

- Esta infraestructura se adecua a un volumen de usuarios de miles a un millón, debido al servicio de cómputo utilizado pueden ser demasiadas solicitudes para la arquitectura.
- Si es necesario almacenar credenciales o contraseñas hacia otros servicios se almacenarán en el servicio de secretos de AWS.
- La configuración básica de cyberseguridad y redes ya se encuentra desplegada ya que no es el foco de este proyecto.

### Ventajas

- **Escalabilidad**: La arquitectura serverless permite escalar el procesamiento según el volumen de imágenes y los requerimientos de los usuarios..
- **Costos optimizados**: Se paga solo por el uso de las funciones Lambda y almacenamiento en S3.
- **Simplicidad**: El uso de servicios administrados por AWS reduce la complejidad operativa ya que no hay que hacer configuraciones ni actualizaciones.

### Desventajas

- **Límite de tiempo de ejecución de Lambda**: Procesar imágenes muy grandes podría requerir ajustar los tiempos de ejecución de Lambda.
- **Dependencia de servicios de AWS**: Esta solución está diseñada y desarrollada para  AWS, lo que puede ser una limitación en entornos multi-cloud.

### Puntos de mejora

- Usar la clase de almacenamiento adecuada para los buckets de S3 según las necesidades de la aplicación, por ahora se está usando el simple storage pero dependiendo de la fecuencia de acceso a las imágenes podrían moverse a una capa Intelligent Tiering o Standard-IA.
-  Si se requiere mayor tiempo o capacidad de procesamiento sería adecuado implementar la solución en un servicio como una instancia de EC2 o un job de Glue que permita mayor cantidad de tiempo de procesamiento.
- Tener en cuenta siempre las recomendaciones de seguridad de AWS, la distribución de roles y permisos hacia los diferentes servicios y conservar siempre el principio de menor privilegio.
- Agregar variables de entorno a la función lambda para simplificar el código y hacerlo más entendible y organizado.


