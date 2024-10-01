/* ---------------------------------------------------------------
 * --------------------- SISTEMA CONTABLE ------------------------
 * --------------------------------------------------------------- */
 
 
-- TABLAS

DROP TABLE IF EXISTS cuentas CASCADE;
DROP TABLE IF EXISTS cuenta_tipos CASCADE;
DROP TABLE IF EXISTS registros CASCADE;
DROP TABLE IF EXISTS monedas CASCADE;
DROP TABLE IF EXISTS transacciones CASCADE;
DROP TABLE IF EXISTS situacion_financiera CASCADE;
DROP TABLE IF EXISTS mayores CASCADE;
DROP TABLE IF EXISTS estado_resultados CASCADE;

-- TABLAS PARA CUENTAS

CREATE TABLE cuenta_tipos
(
	"CuentaTipo_Id" SMALLINT PRIMARY KEY,
	"CuentaTipo_Nom" VARCHAR(35)
);

CREATE TABLE cuentas
(
	"Cuenta_Id" SMALLINT PRIMARY KEY,
	"Cuenta_CuentaTipoId" SMALLINT,
	"Cuenta_Nom" VARCHAR(100),
	FOREIGN KEY ("Cuenta_CuentaTipoId") REFERENCES cuenta_tipos("CuentaTipo_Id")
);


-- TABLAS PARA REGISTROS

CREATE TABLE monedas
(
	"Moneda_Id" SMALLINT PRIMARY KEY,
	"Moneda_Nom" VARCHAR(25),
	"Moneda_Simb" VARCHAR(5)
);

CREATE TABLE registros
(
	"Reg_Id" SERIAL PRIMARY KEY,
	"Reg_MonedaId" SMALLINT,
	"Reg_SaldoIncial" NUMERIC(15, 2),
	"Reg_Fecha" DATE,
	FOREIGN KEY ("Reg_MonedaId") REFERENCES monedas("Moneda_Id")
);


-- TABLAS PARA TRANSACCIONES

CREATE TABLE transacciones
(
    "Tran_Id" SERIAL PRIMARY KEY,
	"Tran_RegId" INTEGER,
	"Tran_CuentaId" SMALLINT,
	"Tran_MontoDeb" NUMERIC(15, 2) DEFAULT 0,
	"Tran_MontoCre" NUMERIC(15, 2) DEFAULT 0,
	"Tran_Fecha" DATE,
	FOREIGN KEY ("Tran_RegId") REFERENCES registros("Reg_Id"),
	FOREIGN KEY ("Tran_CuentaId") REFERENCES cuentas("Cuenta_Id")
);


-- TABLAS PARA MAYORES

CREATE TABLE mayores
(
    "May_Id" SERIAL PRIMARY KEY,
	"May_RegId" INTEGER,
	"May_CuentaId" SMALLINT,
	"May_MontoDeb" NUMERIC(15, 2) DEFAULT 0,
	"May_MontoCre" NUMERIC(15, 2) DEFAULT 0,
	FOREIGN KEY ("May_RegId") REFERENCES registros("Reg_Id"),
	FOREIGN KEY ("May_CuentaId") REFERENCES cuentas("Cuenta_Id")
);

-- TABLAS PARA ESTADO DE RESULTADO

CREATE TABLE estado_resultados
(
    "EstRes_Id" SERIAL PRIMARY KEY,
	"EstRes_RegId" INTEGER,
	"EstRes_Venta" NUMERIC(15, 2),
    "EstRes_CostoVenta" NUMERIC(15, 2),
    "EstRes_UtilidadBruta" NUMERIC(15, 2),
    "EstRes_GastosVenta" NUMERIC(15, 2),
    "EstRes_GastosAdmi" NUMERIC(15, 2),
    "EstRes_UtilidadOper" NUMERIC(15, 2),
    "EstRes_OtrosIngresosGastos" NUMERIC(15, 2),
    "EstRes_GastosFinancieros" NUMERIC(15, 2),
    "EstRes_UtilidadAnteImpuestos" NUMERIC(15, 2),
    "EstRes_ParticipacionTrab" NUMERIC(15, 2),
    "EstRes_ImpuestoRentaGanancia" NUMERIC(15, 2),
    "EstRes_UtilidadNeta" NUMERIC(15, 2),
	FOREIGN KEY ("EstRes_RegId") REFERENCES registros("Reg_Id")
);


