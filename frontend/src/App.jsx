import React, { useState, useEffect } from 'react';
import { api } from './services/api';
import { jsPDF } from "jspdf";
import autoTable from 'jspdf-autotable';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const StatCard = ({ title, value, colorClass }) => (
  <div className={`bg-white p-6 rounded-3xl shadow-sm border-b-4 ${colorClass} flex-1 min-w-[150px]`}>
    <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">{title}</p>
    <p className={`text-3xl font-black ${colorClass.replace('border-', 'text-')}`}>{value}</p>
  </div>
);

export default function App() {
  const [datosAgrupados, setDatosAgrupados] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [loading, setLoading] = useState(true);
  const [modalInfo, setModalInfo] = useState(null);
  const [modalAviso, setModalAviso] = useState(false);
  const [reporteData, setReporteData] = useState({ empresa: "", notas: "" });

  useEffect(() => { cargarTodo(); }, []);

  const cargarTodo = async () => {
    try {
      const docs = await api.obtenerDocumentos();
      const mapa = {};
      docs.forEach(doc => {
        const empresa = doc.cliente_nombre || "Empresa";
        if (!mapa[empresa]) mapa[empresa] = { nombre: empresa, tramites: {}, colores: new Set() };
        const tNombre = (doc.tipo_nombre || "Trámite").toLowerCase();
        const color = (doc.color_estado || "Gris").toLowerCase().trim();
        mapa[empresa].colores.add(color);
        const dataDoc = { ...doc, tipo_display: doc.tipo_nombre || "Trámite" };
        
        if (tNombre.includes('extintor') || tNombre.includes('bomber')) mapa[empresa].tramites.bomberos = dataDoc;
        else if (tNombre.includes('predial')) mapa[empresa].tramites.predial = dataDoc;
        else if (tNombre.includes('licencia')) mapa[empresa].tramites.licencia = dataDoc;
        else mapa[empresa].tramites.otro = dataDoc;
      });
      setDatosAgrupados(Object.values(mapa));
      setLoading(false);
    } catch (e) { setLoading(false); }
  };

  const generarAvisoPDF = () => {
    const doc = new jsPDF();
    const e = datosAgrupados.find(emp => emp.nombre === reporteData.empresa);
    
    doc.setFillColor(30, 41, 59);
    doc.rect(0, 0, 210, 40, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(22);
    doc.text("AVISO DE CONTROL CENTRAL", 14, 25);
    
    doc.setTextColor(40, 40, 40);
    doc.setFontSize(14);
    doc.text(`ATENCIÓN: ${reporteData.empresa}`, 14, 55);
    doc.setFontSize(10);
    doc.text(`FECHA: ${new Date().toLocaleDateString()}`, 14, 62);
    
    doc.setFontSize(11);
    doc.text("OBSERVACIONES DEL DEPARTAMENTO:", 14, 75);
    const splitText = doc.splitTextToSize(reporteData.notas, 180);
    doc.text(splitText, 14, 82);

    if (e) {
      const filas = Object.values(e.tramites).map(t => [t.tipo_display, t.estado_nombre, t.fecha_vencimiento || '---']);
      autoTable(doc, { startY: 100, head: [['Trámite', 'Estatus', 'Vencimiento']], body: filas, headStyles: { fillColor: [79, 70, 229] } });
    }

    doc.save(`Aviso_${reporteData.empresa}.pdf`);
    setModalAviso(false);
    setReporteData({ empresa: "", notas: "" });
  };

  const countV = datosAgrupados.filter(e => e.colores.has('verde')).length;
  const countA = datosAgrupados.filter(e => e.colores.has('amarillo')).length;
  const countR = datosAgrupados.filter(e => e.colores.has('rojo')).length;
  const datosGrafico = [
    { name: 'Vigentes', value: countV, color: '#10b981' },
    { name: 'A Vencer', value: countA, color: '#f59e0b' },
    { name: 'Urgentes', value: countR, color: '#ef4444' },
  ].filter(d => d.value > 0);

  return (
    <div className="min-h-screen bg-slate-50 p-8 md:p-12 font-sans text-slate-800">
      <header className="flex justify-between items-center mb-10">
        <h1 className="text-4xl font-black uppercase italic tracking-tighter">Control Central</h1>
        <button onClick={() => setModalAviso(true)} className="bg-slate-900 text-white px-8 py-4 rounded-full font-black text-xs uppercase shadow-xl hover:bg-indigo-600 transition-all flex items-center gap-2">
          📝 REDACTAR REPORTE
        </button>
      </header>

      <div className="flex flex-wrap gap-4 mb-8">
        <StatCard title="Empresas" value={datosAgrupados.length} colorClass="border-slate-200" />
        <StatCard title="Vigentes" value={countV} colorClass="border-emerald-400" />
        <StatCard title="A Vencer" value={countA} colorClass="border-amber-400" />
        <StatCard title="Urgentes" value={countR} colorClass="border-rose-400" />
      </div>

      <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100 mb-8 flex flex-col md:flex-row items-center justify-between">
        <div>
          <h3 className="text-xl font-black uppercase italic tracking-tighter">Resumen Operativo</h3>
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest italic">Estado global de documentos</p>
        </div>
        <div className="h-[220px] w-full md:w-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={datosGrafico} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                {datosGrafico.map((entry, index) => <Cell key={index} fill={entry.color} stroke="none" />)}
              </Pie>
              <Tooltip contentStyle={{borderRadius: '15px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'}} />
              <Legend verticalAlign="bottom" iconType="circle" wrapperStyle={{ fontSize: '10px', fontWeight: 'bold', textTransform: 'uppercase' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <input type="text" placeholder="Buscar empresa..." className="w-full p-5 mb-8 bg-white rounded-2xl shadow-sm border border-slate-100 outline-none font-bold text-xs uppercase" onChange={(e) => setBusqueda(e.target.value)} />

      <div className="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="bg-slate-50 text-[10px] font-black text-slate-400 uppercase tracking-widest border-b">
              <th className="py-6 px-10">Empresa</th>
              <th className="py-6 px-4 text-center">Predial</th>
              <th className="py-6 px-4 text-center">Licencia</th>
              <th className="py-6 px-4 text-center">Bomberos</th>
              <th className="py-6 px-10 text-center">Otros</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-50">
            {datosAgrupados.filter(e => e.nombre.toLowerCase().includes(busqueda.toLowerCase())).map((e, i) => (
              <tr key={i} className="hover:bg-indigo-50/50 transition-colors group">
                <td className="py-8 px-10 font-black text-slate-700 text-sm uppercase italic group-hover:text-indigo-600 transition-colors">{e.nombre}</td>
                {['predial', 'licencia', 'bomberos', 'otro'].map(t => (
                  <td key={t} className="py-8 px-4 text-center">
                    {e.tramites[t] ? (
                      <div onClick={() => setModalInfo(e.tramites[t])} className={`inline-block px-4 py-1.5 rounded-full border text-[9px] font-black uppercase cursor-pointer hover:scale-110 transition-transform shadow-sm ${e.tramites[t].color_estado?.toLowerCase() === 'verde' ? 'bg-emerald-50 text-emerald-500 border-emerald-100' : e.tramites[t].color_estado?.toLowerCase() === 'rojo' ? 'bg-rose-50 text-rose-500 border-rose-100' : 'bg-amber-50 text-amber-500 border-amber-100'}`}>
                        {e.tramites[t].fecha_vencimiento || e.tramites[t].estado_nombre}
                      </div>
                    ) : <span className="text-slate-200 font-black">-</span>}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* MODAL DETALLES TRÁMITE */}
      {modalInfo && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white rounded-[2.5rem] w-full max-w-md shadow-2xl overflow-hidden animate-in zoom-in duration-200">
            <div className={`p-8 text-white font-black uppercase italic text-xl ${modalInfo.color_estado?.toLowerCase() === 'rojo' ? 'bg-rose-500' : modalInfo.color_estado?.toLowerCase() === 'verde' ? 'bg-emerald-500' : 'bg-amber-500'}`}>{modalInfo.tipo_display}</div>
            <div className="p-8 space-y-4">
              <div className="bg-slate-50 p-6 rounded-2xl">
                <p className="text-[10px] font-black text-slate-400 uppercase">Estatus</p>
                <p className="font-bold text-slate-700">{modalInfo.estado_nombre}</p>
                <p className="text-[10px] font-black text-slate-400 uppercase mt-4">Vencimiento</p>
                <p className="font-bold text-rose-600">{modalInfo.fecha_vencimiento || '---'}</p>
              </div>
              <button onClick={() => window.open(`http://localhost:8000${modalInfo.archivo}`, '_blank')} className="w-full bg-slate-900 text-white py-4 rounded-2xl font-black text-xs uppercase shadow-lg">👁️ Ver Original</button>
              <button onClick={() => setModalInfo(null)} className="w-full text-slate-400 font-bold text-[10px] uppercase pt-2">Cerrar</button>
            </div>
          </div>
        </div>
      )}

      {}
      {modalAviso && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[200] flex items-center justify-center p-4">
          <div className="bg-white rounded-[2.5rem] w-full max-w-lg shadow-2xl overflow-hidden animate-in zoom-in duration-200">
            <div className="p-8 bg-indigo-600 text-white font-black uppercase italic text-xl">Reporte</div>
            <div className="p-8 space-y-6">
              <div>
                <label className="text-[10px] font-black text-slate-400 uppercase block mb-2">Empresa Destinataria</label>
                <select className="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500" onChange={(e) => setReporteData({...reporteData, empresa: e.target.value})}>
                  <option value="">Selecciona una empresa...</option>
                  {datosAgrupados.map((e, i) => <option key={i} value={e.nombre}>{e.nombre}</option>)}
                </select>
              </div>
              <div>
                <label className="text-[10px] font-black text-slate-400 uppercase block mb-2">Reporte</label>
                <textarea rows="4" className="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Escribe aquí las instrucciones..." onChange={(e) => setReporteData({...reporteData, notas: e.target.value})}></textarea>
              </div>
              <div className="flex gap-4">
                <button onClick={generarAvisoPDF} disabled={!reporteData.empresa || !reporteData.notas} className="flex-1 bg-indigo-600 text-white py-4 rounded-2xl font-black text-xs uppercase shadow-lg disabled:opacity-50">Descargar Aviso</button>
                <button onClick={() => setModalAviso(false)} className="px-6 text-slate-400 font-bold text-[10px] uppercase">Cancelar</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}