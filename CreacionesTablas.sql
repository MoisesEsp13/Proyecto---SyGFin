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
	"Reg_Nombre" VARCHAR(256),
	"Reg_MonedaId" SMALLINT,
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

