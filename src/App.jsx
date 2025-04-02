
import React, { useState } from "react";
import { motion } from "framer-motion";

const API_URL = "https://zuru.onrender.com/classify";

export default function App() {
  const [input, setInput] = useState("");
  const [suggestion, setSuggestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleClassify = async () => {
    if (input.length < 3) return;
    setLoading(true);
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ descripcion: input })
      });
      const data = await response.json();
      setSuggestion(data.categoria || "Sin coincidencias claras");
    } catch (err) {
      setSuggestion("Error al clasificar");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#f3f4f6",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "1rem"
    }}>
      <h1 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "1rem" }}>
        Clasificador de mercancías (IA)
      </h1>
      <input
        type="text"
        placeholder="Describe tu mercancía..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{
          width: "100%",
          maxWidth: "500px",
          marginBottom: "1rem",
          padding: "0.5rem",
          fontSize: "1rem",
          borderRadius: "8px",
          border: "1px solid #ccc"
        }}
      />
      <button
        onClick={handleClassify}
        disabled={loading || input.length < 3}
        style={{
          backgroundColor: "#7c3aed",
          color: "white",
          padding: "0.5rem 1rem",
          borderRadius: "8px",
          border: "none",
          cursor: "pointer",
          marginBottom: "1rem"
        }}
      >
        {loading ? "Clasificando..." : "Clasificar con IA"}
      </button>

      {suggestion && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          style={{
            width: "100%",
            maxWidth: "500px",
            backgroundColor: "white",
            borderRadius: "12px",
            boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
            padding: "1rem"
          }}
        >
          <p style={{ fontSize: "0.875rem", color: "#6b7280" }}>Respuesta de la IA:</p>
          <p style={{ fontSize: "1.125rem", fontWeight: "600" }}>{suggestion}</p>
        </motion.div>
      )}
    </div>
  );
}
