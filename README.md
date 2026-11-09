# Urban Routes - Pruebas Automatizadas
 
## Descripción
 
Proyecto de pruebas automatizadas para la aplicación web Urban Routes, una plataforma para solicitar taxis. Las pruebas cubren el flujo completo de pedido de un taxi, desde la configuración de la ruta hasta la asignación del conductor.
 
## Tecnologías y técnicas utilizadas
 
- Python 3.12
- Selenium WebDriver para la automatización del navegador
- Pytest como framework de pruebas
- Page Object Model (POM) como patrón de diseño para organizar los localizadores y métodos de la página
- WebDriverWait y Expected Conditions para la sincronización con los elementos de la UI
- Chrome DevTools Protocol (CDP) para interceptar el código de confirmación telefónica
 
## Pruebas incluidas
 
1. Configurar la dirección de origen y destino
2. Seleccionar la tarifa Comfort
3. Rellenar el número de teléfono y confirmar con código SMS
4. Agregar una tarjeta de crédito como método de pago
5. Escribir un mensaje para el conductor
6. Solicitar manta y pañuelos
7. Solicitar 2 helados
8. Verificar que aparece el modal de búsqueda de taxi
9. Verificar que aparece la información del conductor asignado
 
## Instrucciones para ejecutar las pruebas
 
1. Clonar el repositorio
 
2. Crear y activar un entorno virtual
```
python3 -m venv .venv
source .venv/bin/activate
```
 
3. Instalar las dependencias
```
pip install selenium pytest
```
 
4. Asegurarse de que el servidor de Urban Routes esté corriendo y actualizar la URL en el archivo `data.py`
 
5. Ejecutar las pruebas
```
pytest main.py -v
```
### comentarios y recomendaciones
En el test de agregar tarjetas de credito en algunos navegadores o sistemas operativos no se puede ejecutar el cerrar el panel al final de la prueba,
en caso de ser asi es necesario hacer click manualmente en la x para visualizar correctamente las demas pruebas y flujos.