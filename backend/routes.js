const express = require('express');
const router = express.Router();

// Importar las conexiones por base de datos
const dev1 = require('./db/dev1');           // dbTREP (THEONE\SQLDEV1)
const dev2 = require('./db/dev2');           // Salto-Trep (THEONE\SQLDEV2)
const devtestico = require('./db/devtestico'); // dboficial (SQLSERVER\DEVTESTICO)


// 📌 /api/trep/departamentos → dbTREP
router.get('/trep/departamentos', async (req, res) => {
  try {
    const pool = await dev1;
    const result = await pool.request().query('SELECT * FROM Department');
    res.json(result.recordset);
  } catch (err) {
    res.status(500).send('Error en dbTREP: ' + err.message);
  }
});


// 📌 /api/salto/departamentos → Salto-Trep
router.get('/salto/departamentos', async (req, res) => {
  try {
    const pool = await dev2;
    const result = await pool.request().query('SELECT * FROM Department');
    res.json(result.recordset);
  } catch (err) {
    res.status(500).send('Error en Salto-Trep: ' + err.message);
  }
});


// 📌 /api/oficial/departamentos → dboficial
router.get('/oficial/departamentos', async (req, res) => {
  try {
    const pool = await devtestico;
    const result = await pool.request().query('SELECT * FROM Department');
    res.json(result.recordset);
  } catch (err) {
    res.status(500).send('Error en dboficial: ' + err.message);
  }
});

module.exports = router;
