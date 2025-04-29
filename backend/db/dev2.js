const sql = require('mssql');

const config = {
  user: 'saCliente',
  password: '123',
  server: 'THEONE',
  port: 7023, // asegúrate de asignar este puerto fijo en la instancia DEV2
  database: 'Salto-Trep',
  options: {
    trustServerCertificate: true,
    encrypt: true
  }
};

const poolPromise = new sql.ConnectionPool(config)
  .connect()
  .then(pool => {
    console.log('✅ Conectado a Salto-Trep (DEV2)');
    return pool;
  })
  .catch(err => {
    console.error('❌ Error en conexión DEV2:', err);
  });

module.exports = poolPromise;
