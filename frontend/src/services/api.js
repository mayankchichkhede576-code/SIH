const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';
async function request(path, options={}) { const r=await fetch(API+path,{headers:{'Content-Type':'application/json'},...options}); const data=await r.json().catch(()=>({detail:r.statusText})); if(!r.ok) throw new Error(data.detail||'Request failed'); return data; }
export const health=()=>request('/health');
export const investigations=()=>request('/investigations');
export const createInvestigation=(body)=>request('/investigations',{method:'POST',body:JSON.stringify(body)});
export const getInvestigation=(id)=>request(`/investigations/${id}`);
export const followup=(id,body)=>request(`/investigations/${id}/followup`,{method:'POST',body:JSON.stringify(body)});
