const API_BASE = "http://localhost:8000/api";

export const api = {
  obtenerDocumentos: async () => {
    const response = await fetch(`${API_BASE}/documentos/`);
    if (!response.ok) throw new Error("No se pudo conectar con Django");
    return await response.json();
  },
  actualizarDocumento: async (id, formData) => {
    const response = await fetch(`${API_BASE}/documentos/${id}/`, {
      method: 'PATCH',
      body: formData,
    });
    return await response.json();
  }
};