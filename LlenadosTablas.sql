/* ---------------------------------------------------------------
 * --------------------- SISTEMA CONTABLE ------------------------
 * --------------------------------------------------------------- */


-- DATOS PARA CUENTAS

INSERT INTO cuenta_tipos (
    "CuentaTipo_Id", "CuentaTipo_Nom")
VALUES 
    (1, 'Activo Corriente'),
    (2, 'Activo Corriente (Existencias)'),
    (3, 'Activo No Corriente'),
    (4, 'Pasivo'),
    (5, 'Patrimonio'),
    (6, 'Gastos'),
    (7, 'Ingreso'),
    (8, 'Cuentas de Cierre'),
    (9, 'Cuentas Analíticas de Explotación');

INSERT INTO cuentas (
    "Cuenta_Id", "Cuenta_CuentaTipoId", "Cuenta_Nom")
VALUES 
    (10, 1, 'Efectivo y Equivalentes de Efectivo'),
    (11, 1, 'Inversiones Financieras'),
    (12, 1, 'Cuentas Por Cobrar Comerciales – Terceros'),
    (13, 1, 'Cuentas Por Cobrar Comerciales – Relacionadas'),
    (14, 1, 'Cuentas Por Cobrar al Personal, a los Accionistas, Directores y Gerentes'),
    (16, 1, 'Cuentas Por Cobrar Diversas – Terceros'),
    (17, 1, 'Cuentas Por Cobrar Diversas – Relacionadas'),
    (18, 1, 'Servicios y Otros Contratados Por Anticipado'),
    (20, 2, 'Mercaderías'),
    (21, 2, 'Productos Terminados'),
    (22, 2, 'Subproductos, Desechos y Desperdicios'),
    (23, 2, 'Productos en Proceso'),
    (24, 2, 'Materias Primas'),
    (25, 2, 'Materiales Auxiliares, Suministros y Repuestos'),
    (26, 2, 'Envases y Embalajes'),
    (27, 2, 'Activos No Corrientes Mantenidos para la Venta'),
    (28, 2, 'Existencias Por Recibir'),
    (29, 2, 'Desvalorización de Existencias'),
    (30, 3, 'Inversiones Mobiliarias'),
    (31, 3, 'Inversiones Inmobiliarias'),
    (32, 3, 'Activos Adquiridos en Arrendamiento Financiero'),
    (33, 3, 'Inmuebles, Maquinaria y Equipo'),
    (34, 3, 'Intangibles'),
    (35, 3, 'Activos Biológicos'),
    (36, 3, 'Desvalorización de Activo Inmovilizado'),
    (37, 3, 'Activo Diferido'),
    (38, 3, 'Otros Activos'),
    (39, 3, 'Depreciación, Amortización y Agotamiento Acumulados'),
    (40, 4, 'Tributos y Aportes al Sistema de Pensiones y de Salud Por Pagar'),
    (41, 4, 'Remuneraciones y Participaciones Por Pagar'),
    (42, 4, 'Cuentas Por Pagar Comerciales – Terceros'),
    (43, 4, 'Cuentas Por Pagar Comerciales – Relacionadas'),
    (44, 4, 'Cuentas Por Pagar a los Accionistas, Directores y Gerentes'),
    (45, 4, 'Obligaciones Financieras'),
    (46, 4, 'Cuentas Por Pagar Diversas – Terceros'),
    (47, 4, 'Cuentas Por Pagar Diversas – Relacionadas'),
    (48, 4, 'Provisiones'),
    (49, 4, 'Pasivo Diferido'),
    (50, 5, 'Capital'),
    (51, 5, 'Acciones de Inversión'),
    (52, 5, 'Capital Adicional'),
    (56, 5, 'Resultados No Realizados'),
    (57, 5, 'Excedente de Revaluación'),
    (58, 5, 'Reservas'),
    (60, 6, 'Compras'),
    (61, 6, 'Variación de Existencias'),
    (62, 6, 'Gastos de Personal, Directores y Gerentes'),
    (63, 6, 'Gastos de Servicios Prestados Por Terceros'),
    (64, 6, 'Gastos Por Tributos'),
    (65, 6, 'Otros Gastos De Gestión'),
    (66, 6, 'Pérdida Por Medición de Activos No Financieros al Valor Razonable'),
    (67, 6, 'Gastos Financieros'),
    (68, 6, 'Valuación y Deterioro de Activos y Provisiones'),
    (69, 6, 'Costo De Ventas'),
    (70, 7, 'Ventas'),
    (71, 7, 'Variación de la Producción Almacenada'),
    (72, 7, 'Producción de Activo Inmovilizado'),
    (73, 7, 'Descuentos, Rebajas y Bonificaciones Obtenidos'),
    (74, 7, 'Descuentos, Rebajas y Bonificaciones Concedidos'),
    (75, 7, 'Otros Ingresos de Gestión'),
    (76, 7, 'Ganancia Por Medición de Activos No Financieros al Valor Razonable'),
    (77, 7, 'Ingresos Financieros'),
    (78, 7, 'Cargas Cubiertas Por Provisiones'),
    (79, 7, 'Cargas Imputables a Cuentas de Costos y Gastos'),
    (81, 8, 'Producción del Ejercicio'),
    (82, 8, 'Valor Agregado'),
    (83, 8, 'Excedente Bruto de Explotación'),
    (84, 8, 'Resultado de Explotación'),
    (85, 8, 'Resultado Antes de Participaciones e Impuestos'),
    (87, 8, 'Participaciones de los Trabajadores'),
    (88, 8, 'Impuesto a la Renta'),
    (89, 8, 'Determinación del Resultado del Ejercicio'),
    (91, 9, ' Costos Por Distribuir'),
    (92, 9, 'Costos de Producción'),
    (93, 9, 'Centros de Costos'),
    (94, 9, 'Gastos Administrativos'),
    (95, 9, 'Gastos de Ventas'),
    (96, 9, 'Gastos Financieros');
	

-- DATOS PARA REGISTROS

INSERT INTO monedas(
	"Moneda_Id", "Moneda_Nom", "Moneda_Simb")
VALUES 
	(1, 'soles', 'S/.'),
	(2, 'dólares', '$');
