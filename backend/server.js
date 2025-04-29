const express = require('express');
const cors = require('cors');
const rutas = require('./routes');

const app = express();
app.use(cors());
app.use(express.json());
app.use('/api', rutas);

const PORT = 4000;
app.listen(PORT, () => {
  console.log(`🚀 API corriendo en http://localhost:${PORT}`);
});
