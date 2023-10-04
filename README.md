# Uso
ejecutar el comando ´docker-compose up -d´
para corre el proyecto    

esto levantara el servidor de MySQL, ejecutando el scrip en donde pasa el exel al la Base de Datos covi 

ademas de leventar la api en el pueto 80


## Consultas del SQL
secreo el procedure donde enlista los registros y filtros de estos para eso usamos el precedure `consulta` en donde le pasaremos los siguintes datos  

*edad_param*: donde 0 es igual a todos, -1 son los niños, -2 son adolecentes, -3 adultos, -4 adultos mayores  
*sexo_param*: donde le pasamos los datos `T`, `M`, `F`  
*entidad_param*: donde pasamos `Todas`, los nombres de las entidades  

### ejemplo
```sql
CALL Covid.consulta(-1, 'T', 'Todas'); -- Ejemplo: Sin filtros

CALL Covid.consulta(0, 'M', 'Ciudad de México'); -- Ejemplo: Filtrar por sexo masculino y entidad específica

CALL Covid.consulta(0, 'M', 'Todas'); -- Ejemplo: Filtrar por edad (adolescentes) y todos los sexos
```
## api

La api cuenta con 2 metos `http://localhost:5000/consulta` `GET` y `POST`. Donde en el get solo ingresas la url y te trae un listado de todos los caso, en el `POST` le mandamos los datos `edad`, `sexo`, `entida` nos traera los casos filtrados

`GET`
```sh
http://localhost:5000/consulta

```
`POST`
```sh
http://localhost:5000/consulta


{
    "edad": 0,
    "sexo": "T",
    "entidad": "Todas"
}

```