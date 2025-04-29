import { useState, useEffect } from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';

// Registrar los componentes de Chart.js
ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

// Datos de recintos (simulados a partir de Datos.xlsx)
const recintosData = [
  { CodigoRecintoElectoral: 1, CodigoDistribucionTerritorial: 10101, Nombre: "U.E. Santa Mónica", Direccion: "Calle Achanq’ara entre las calles Chariña y Qoyllur, OTB Ticti Norte" },
  { CodigoRecintoElectoral: 2, CodigoDistribucionTerritorial: 10102, Nombre: "U.E. Padresama", Direccion: "Se encuentra sobre la carretera cochabamba a Santa Cruz km 150, sindicato agrario Padresama" },
  { CodigoRecintoElectoral: 3, CodigoDistribucionTerritorial: 10103, Nombre: "U.E. Lacolaconi", Direccion: "Lacolaconi" },
  // ... (continúa con los demás recintos, pero para este ejemplo usaremos solo los primeros para simplificar)
  { CodigoRecintoElectoral: 316, CodigoDistribucionTerritorial: 20607, Nombre: "Escuela Isaac Attie", Direccion: "Linde–Chiquicollo" },
];

// Datos de actas electorales (simulados y expandidos a partir del fragmento)
const actasData = [
  { CodigoRecintoElectoral: 1, Mesa: 1, Votos: { "MAS-IPSP": 200, "SUMATe": 150, "VOTEXCHI": 100, "CHUPACOTO": 50 } },
  { CodigoRecintoElectoral: 1, Mesa: 2, Votos: { "MAS-IPSP": 180, "SUMATe": 120, "VOTEXCHI": 80, "CHUPACOTO": 40 } },
  { CodigoRecintoElectoral: 2, Mesa: 1, Votos: { "MAS-IPSP": 250, "SUMATe": 100, "VOTEXCHI": 90, "CHUPACOTO": 60 } },
  { CodigoRecintoElectoral: 2, Mesa: 2, Votos: { "MAS-IPSP": 220, "SUMATe": 110, "VOTEXCHI": 70, "CHUPACOTO": 30 } },
  // ... (simulamos datos para los primeros recintos)
  { CodigoRecintoElectoral: 316, Mesa: 1, Votos: { "MAS-IPSP": 300, "SUMATe": 200, "VOTEXCHI": 150, "CHUPACOTO": 100 } },
];

// Departamentos (basados en el primer dígito del CodigoDistribucionTerritorial)
const departamentos = [
  { id: 1, nombre: "Cochabamba" },
  { id: 2, nombre: "La Paz" },
  // ... (simplificado para este ejemplo)
];

function App() {
  const [selectedDepartamento, setSelectedDepartamento] = useState("");
  const [selectedRecinto, setSelectedRecinto] = useState("");
  const [selectedMesa, setSelectedMesa] = useState("");
  const [selectedPartido, setSelectedPartido] = useState("");

  // Filtrar recintos por departamento
  const filteredRecintos = selectedDepartamento
    ? recintosData.filter(r => Math.floor(r.CodigoDistribucionTerritorial / 10000) === parseInt(selectedDepartamento))
    : recintosData;

  // Filtrar actas por recinto y mesa
  const filteredActas = actasData.filter(acta => {
    let match = true;
    if (selectedRecinto) match = match && acta.CodigoRecintoElectoral === parseInt(selectedRecinto);
    if (selectedMesa) match = match && acta.Mesa === parseInt(selectedMesa);
    return match;
  });

  // Calcular votos totales por partido
  const voteData = filteredActas.reduce((acc, acta) => {
    Object.keys(acta.Votos).forEach(partido => {
      if (!acc.parties[partido]) {
        acc.parties[partido] = { name: partido, votes: 0, color: getColor(partido) };
      }
      acc.parties[partido].votes += acta.Votos[partido];
    });
    return acc;
  }, { parties: {}, blankVotes: 0, nullVotes: 0 });

  const partiesArray = Object.values(voteData.parties).filter(p => !selectedPartido || p.name === selectedPartido);
  const totalParticipants = partiesArray.reduce((sum, party) => sum + party.votes, 0) + voteData.blankVotes + voteData.nullVotes;

  // Datos para las gráficas
  const barData = {
    labels: partiesArray.map(p => p.name),
    datasets: [{
      label: 'Votos',
      data: partiesArray.map(p => p.votes),
      backgroundColor: partiesArray.map(p => p.color),
      borderColor: partiesArray.map(p => p.color),
      borderWidth: 1,
    }],
  };

  const pieData = {
    labels: [...partiesArray.map(p => p.name), 'Blancos', 'Nulos'],
    datasets: [{
      data: [...partiesArray.map(p => p.votes), voteData.blankVotes, voteData.nullVotes],
      backgroundColor: [...partiesArray.map(p => p.color), '#D3D3D3', '#696969'],
    }],
  };

  const statsBarData = {
    labels: ['Votos válidos', 'Votos blancos', 'Votos nulos'],
    datasets: [{
      label: 'Porcentaje',
      data: [
        (partiesArray.reduce((sum, party) => sum + party.votes, 0) / totalParticipants) * 100,
        (voteData.blankVotes / totalParticipants) * 100,
        (voteData.nullVotes / totalParticipants) * 100,
      ],
      backgroundColor: ['#1E90FF', '#D3D3D3', '#696969'],
      borderColor: ['#1E90FF', '#D3D3D3', '#696969'],
      borderWidth: 1,
    }],
  };

  const chartOptions = {
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Votos por Partido',
        font: { size: 18, weight: 'bold' },
        padding: { top: 10, bottom: 30 },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Votos' },
        ticks: { stepSize: 200 },
      },
    },
    animation: {
      duration: 2000,
      easing: 'easeInOutQuart',
    },
  };

  const pieOptions = {
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          pointStyle: 'circle',
          padding: 20,
          font: { size: 14 },
        },
      },
      tooltip: { enabled: true },
    },
    animation: {
      duration: 2000,
      easing: 'easeInOutQuart',
    },
  };

  const statsBarOptions = {
    indexAxis: 'y',
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: '',
        font: { size: 18, weight: 'bold' },
        padding: { top: 10, bottom: 30 },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: (value) => `${value}%`,
        },
      },
    },
    animation: {
      duration: 2000,
      easing: 'easeInOutQuart',
    },
    elements: {
      bar: {
        borderRadius: 5,
      },
    },
  };

  const validVotesPercentage = ((partiesArray.reduce((sum, party) => sum + party.votes, 0) / totalParticipants) * 100).toFixed(1);
  const blankVotesPercentage = ((voteData.blankVotes / totalParticipants) * 100).toFixed(1);
  const nullVotesPercentage = ((voteData.nullVotes / totalParticipants) * 100).toFixed(1);

  const titleText = "ELECCIONES PRESIDENCIALES TREP";
  const trepColors = ['#e74c3c', '#f1c40f', '#16a085', '#e74c3c'];

  // Función para obtener el color de cada partido
  function getColor(partido) {
    const colors = {
      "MAS-IPSP": "#1E90FF",
      "SUMATe": "#FFD700",
      "VOTEXCHI": "#FF4500",
      "CHUPACOTO": "#32CD32",
    };
    return colors[partido] || "#000000";
  }

  // Opciones para los filtros
  const mesasDisponibles = [...new Set(actasData
    .filter(a => !selectedRecinto || a.CodigoRecintoElectoral === parseInt(selectedRecinto))
    .map(a => a.Mesa))].sort((a, b) => a - b);

  const partidosDisponibles = [...new Set(Object.keys(actasData[0].Votos))];

  return (
    <div className="container">
      <div className="header-decoration"></div>
      <h1 className="title">
        {Array.from(titleText).map((char, index) => {
          const isTrep = index >= titleText.length - 4;
          return (
            <span
              key={index}
              className={isTrep ? 'trep-letter' : 'black-text'}
              style={isTrep ? { color: trepColors[titleText.length - 1 - index] } : {}}
            >
              {char}
            </span>
          );
        })}
      </h1>

      <div className="filters">
        <div className="filter-group">
          <label>Departamento:</label>
          <select value={selectedDepartamento} onChange={e => { setSelectedDepartamento(e.target.value); setSelectedRecinto(""); setSelectedMesa(""); }}>
            <option value="">Todos</option>
            {departamentos.map(dep => (
              <option key={dep.id} value={dep.id}>{dep.nombre}</option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label>Recinto:</label>
          <select value={selectedRecinto} onChange={e => { setSelectedRecinto(e.target.value); setSelectedMesa(""); }}>
            <option value="">Todos</option>
            {filteredRecintos.map(r => (
              <option key={r.CodigoRecintoElectoral} value={r.CodigoRecintoElectoral}>{r.Nombre}</option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label>Mesa:</label>
          <select value={selectedMesa} onChange={e => setSelectedMesa(e.target.value)}>
            <option value="">Todas</option>
            {mesasDisponibles.map(mesa => (
              <option key={mesa} value={mesa}>{mesa}</option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label>Partido:</label>
          <select value={selectedPartido} onChange={e => setSelectedPartido(e.target.value)}>
            <option value="">Todos</option>
            {partidosDisponibles.map(partido => (
              <option key={partido} value={partido}>{partido}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="content">
        <h2 className="total">
          Total de Participantes: <span className="highlight">{totalParticipants.toLocaleString()}</span>
        </h2>

        <div className="charts">
          <div className="chart-box fade-in-left">
            <Bar data={barData} options={chartOptions} />
          </div>
          <div className="chart-box fade-in-right">
            <h3>Distribución de Votos</h3>
            <Pie data={pieData} options={pieOptions} className="rotate-on-load" />
          </div>
        </div>

        <div className="stats-bar fade-in">
          <Bar data={statsBarData} options={statsBarOptions} height={100} />
          <div className="stats-text">
            <p>Votos válidos: <span className="highlight">{validVotesPercentage}%</span></p>
            <p>Votos blancos: <span className="highlight">{blankVotesPercentage}%</span></p>
            <p>Votos nulos: <span className="highlight">{nullVotesPercentage}%</span></p>
          </div>
        </div>

        <div className="additional-stats">
          <p className="participation">Participación: <span className="highlight">78.3%</span></p>
        </div>
      </div>

      <footer className="footer fade-in">
        <p>Desarrollado con ❤️ para Bolivia <span className="bolivia-flag">🇧🇴</span></p>
      </footer>
    </div>
  );
}

export default App;