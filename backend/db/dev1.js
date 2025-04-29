const sql = require('mssql');

const config = {
  user: 'saServer',
  password: '123',
  server: 'THEONE',
  port: 7022,
  database: 'dbTREP',
  options: {
    trustServerCertificate: true,
    encrypt: true
  }
};

const poolPromise = new sql.ConnectionPool(config)
  .connect()
  .then(pool => {
    console.log('✅ Conectado a dbTREP (DEV1)');
    return pool;
  })
  .catch(err => {
    console.error('❌ Error en conexión DEV1:', err);
  });

module.exports = poolPromise;
