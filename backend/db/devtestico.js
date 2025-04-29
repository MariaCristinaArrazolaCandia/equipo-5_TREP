const sql = require('mssql');

const config = {
  user: 'sa',
  password: '123',
  server: 'SQLTESTIGO',
  port: 7024, // asegúrate de asignar este puerto fijo a la instancia DEVTESTICO
  database: 'dboficial',
  options: {
    trustServerCertificate: true,
    encrypt: true
  }
};

const poolPromise = new sql.ConnectionPool(config)
  .connect()
  .then(pool => {
    console.log('✅ Conectado a dboficial (DEVTESTICO)');
    return pool;
  })
  .catch(err => {
    console.error('❌ Error en conexión DEVTESTICO:', err);
  });

module.exports = poolPromise;
