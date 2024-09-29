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
    (4, 'Pasivos'),
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
    (13, 1, 'Cuentas Por Cobrar Comerciales – Relacionadas');
	

-- DATOS PARA REGISTROS

INSERT INTO monedas(
	"Moneda_Id", "Moneda_Nom", "Moneda_Simb")
VALUES 
	(1, 'soles', 'S/.'),
	(2, 'dólares', '$');
	
INSERT INTO registros(
	"Reg_MonedaId", "Reg_SaldoIncial", "Reg_Fecha")
VALUES 
	(1, 2000, '27/09/24');


-- DATOS PARA TRANSACCIONES

INSERT INTO transacciones(
	"Tran_RegId", "Tran_CuentaId", "Tran_MontoDeb", "Tran_MontoCre", "Tran_Fecha")
VALUES
	(?, ?, ?, ?, ?);


-- DATOS PARA MAYORES

INSERT INTO mayores(
	"May_RegId", "May_CuentaId", "May_MontoDeb", "May_MontoCre")
VALUES 
	(?, ?, ?, ?);


-- DATOS PARA ESTADO DE SITUACIÓN FINANCIERA

INSERT INTO situacion_financiera(
	"SitFin_RegId", "SitFin_TotalActCorr", "SitFin_TotalActNoCorr", "SitFin_TotalAct", "SitFin_TotalPasCorr", "SitFin_TotalPasNoCorr", "SitFin_TotalPas", "SitFin_TotalPatrimonio")
	VALUES (?, ?, ?, ?, ?, ?, ?, ?);



-- TABLAS PARA ESTADO DE RESULTADO

INSERT INTO estado_resultados(
	"EstRes_RegId", "EstRes_Venta", "EstRes_CostoVenta", "EstRes_UtilidadBruta", "EstRes_GastosVenta", "EstRes_GastosAdmi", "EstRes_UtilidadOper", "EstRes_OtrosIngresosGastos", "EstRes_GastosFinancieros", "EstRes_UtilidadAnteImpuestos", "EstRes_ParticipacionTrab", "EstRes_ImpuestoRentaGanancia", "EstRes_UtilidadNeta")
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

