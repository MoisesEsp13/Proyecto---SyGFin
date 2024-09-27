/* ---------------------------------------------------------------
 * --------------------- SISTEMA CONTABLE ------------------------
 * --------------------------------------------------------------- */


-- DATOS PARA CUENTAS

INSERT INTO cuenta_tipos(
	"CuentaTipo_Id", "CuentaTipo_Nom")
VALUES 
	(?, ?);

INSERT INTO cuentas(
	"Cuenta_Id", "Cuenta_CuentaTipoId", "Cuenta_Nom")
VALUES 
	(?, ?, ?);
	

-- DATOS PARA REGISTROS

INSERT INTO monedas(
	"Moneda_Id", "Moneda_Nom", "Moneda_Simb")
VALUES 
	(?, ?, ?);
	
INSERT INTO registros(
	"Reg_MonedaId", "Reg_SaldoIncial", "Reg_Fecha")
VALUES 
	(?, ?, ?);


-- DATOS PARA TRANSACCIONES

INSERT INTO transacciones(
	"Tran_RegId", "Tran_CuentaId", "Tran_Monto", "Tran_IsAumento", "Tran_Fecha")
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

