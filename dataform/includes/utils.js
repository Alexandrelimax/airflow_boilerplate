module.exports = {
    // Já existente
    getTodayPartition: () => {
        const today = new Date();
        return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    },

    // 🔹 Helper para filtros comuns
    emailAndCreatedAtNotNull: () => `email IS NOT NULL AND created_at IS NOT NULL`,

    // 🔹 Helper para lógica incremental (condicional WHERE)
    incrementalWhereClause: (field = "updated_at") => `
      {% if is_incremental() %}
        WHERE ${field} > (SELECT MAX(${field}) FROM {{ this }})
      {% endif %}
    `,
};
