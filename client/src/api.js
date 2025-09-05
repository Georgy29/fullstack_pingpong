const BASE = import.meta.env.VITE_API_BASE || '';
export const apiFetch = (path, options) => fetch(`${BASE}${path}`, options);