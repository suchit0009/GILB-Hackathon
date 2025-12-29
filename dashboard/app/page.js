'use client';
import React, { useState, useEffect } from 'react';
import {
    ShieldAlert, Activity, Lock, Users,
    Search, Menu, Bell, Zap, Globe, Power,
    Target, AlertTriangle, CheckCircle, Smartphone
} from 'lucide-react';
import {
    LineChart, Line, AreaChart, Area, XAxis, YAxis,
    CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts';

// --- MOCK CONSTANTS ---
const THREATS = [
    { id: 'T-9901', time: '14:20:05', type: 'HUNDI RING', amount: 1250000, risk: 0.99 },
    { id: 'T-9902', time: '14:20:12', type: 'STRUCTURING', amount: 95000, risk: 0.88 },
    { id: 'T-9903', time: '14:21:45', type: 'MULE ACCT', amount: 4500, risk: 0.72 },
    { id: 'T-9904', time: '14:22:01', type: 'CRYPTO P2P', amount: 250000, risk: 0.95 },
    { id: 'T-9905', time: '14:22:30', type: 'SMURFING', amount: 8200, risk: 0.65 },
];

export default function Dashboard() {
    // Hydration Fix: Start with empty/static data, then populate on client
    const [mounted, setMounted] = useState(false);
    const [tpsHistory, setTpsHistory] = useState([]);
    const [latHistory, setLatHistory] = useState([]);
    const [threats, setThreats] = useState([]);

    // ... (Hooks remain same) ...

    {/* Central Red Mule - Glowing (Dynamic) */ }
    <div className="w-32 h-32 rounded-full bg-red-600/20 border-2 border-red-500 shadow-[0_0_50px_#FF003C] flex flex-col items-center justify-center text-red-500 font-bold text-xs backdrop-blur-sm z-50 relative">
        <div className="absolute inset-0 rounded-full animate-ping bg-red-500/30"></div>
        <span className="text-[10px] text-red-300">DETECTED</span>
        {threats.length > 0 ? threats[0].id : "SCANNING..."}
    </div>

    {/* Connected Nodes */ }
    {
        [...Array(6)].map((_, i) => (
            <div key={i} className="absolute w-12 h-12 bg-slate-900 border border-cyan-500/50 rounded-full flex items-center justify-center text-[10px] text-cyan-300 shadow-[0_0_15px_#00F0FF33]"
                style={{
                    transform: `rotate(${i * 60}deg) translate(180px) rotate(-${i * 60}deg)`,
                }}>
                <div className="absolute top-1/2 left-1/2 w-[180px] h-[1px] bg-gradient-to-l from-cyan-500 to-transparent -z-10 origin-left"
                    style={{ transform: `translate(-50%, -50%) rotate(${i * 60 + 180}deg)` }}></div>
                ACC_{i}0{i}
            </div>
        ))
    }
                            </div >
                        </div >
                    </div >

        {/* THREAT VELOCITY CHART (Bottom Left) */ }
        < div className = "glass-panel h-64 p-4 rounded-lg border border-white/5 relative" >
                        <div className="flex justify-between mb-2">
                            <h3 className="font-bold text-slate-400 flex items-center gap-2"><Activity size={16} /> THREAT VELOCITY (24H)</h3>
                            <span className="text-xs text-red-400 flex items-center gap-1"><AlertTriangle size={12} /> PEAK DETECTED</span>
                        </div>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={tpsHistory.map((d, i) => ({ ...d, fraud: d.val * (i > 40 ? 0.8 : 0.1) }))}>
                                <defs>
                                    <linearGradient id="fraudGrad" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#FF003C" stopOpacity={0.4} />
                                        <stop offset="95%" stopColor="#FF003C" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                <XAxis hide />
                                <YAxis hide />
                                <Tooltip contentStyle={{ backgroundColor: '#020617', borderColor: '#334155' }} itemStyle={{ color: '#fff' }} />
                                <Area type="monotone" dataKey="fraud" stroke="#FF003C" strokeWidth={2} fill="url(#fraudGrad)" />
                                <ReferenceLine x={45} stroke="#FF003C" strokeDasharray="3 3" label={{ position: 'top', value: 'ATTACK START', fill: '#FF003C', fontSize: 10 }} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div >
                </div >

        {/* RIGHT COL: ALERTS + COMMAND ZONE (4 Cols) */ }
        < div className = "lg:col-span-4 flex flex-col gap-4" >

            {/* COMMAND ZONE */ }
            < div className = "glass-panel p-5 rounded-lg border-t-4 border-red-500" >
                        <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                            <Target size={18} className="text-red-500" /> COMMAND ZONE
                        </h3>

                        <div className="space-y-4">
                            <button className="w-full py-4 bg-red-600 hover:bg-red-500 active:scale-[0.98] transition text-white font-bold text-lg tracking-widest rounded shadow-[0_0_20px_rgba(255,0,60,0.4)] flex items-center justify-center gap-3">
                                <Lock size={24} /> FREEZE ASSETS
                            </button>

                            <div className="grid grid-cols-2 gap-3">
                                <ToggleSwitch label="CIRCUIT BREAKER" status={true} />
                                <ToggleSwitch label="HUNTER AGENT" status={true} />
                            </div>
                        </div>
                    </div >

        {/* LIVE THREATS TABLE */ }
        < div className = "glass-panel flex-1 rounded-lg border border-white/5 overflow-hidden flex flex-col" >
                        <div className="p-3 border-b border-white/5 bg-slate-900/50 flex justify-between items-center">
                            <h3 className="font-bold text-cyan-400 flex items-center gap-2"><Search size={16} /> LIVE THREATS</h3>
                            <span className="text-[10px] bg-red-900/30 text-red-400 px-2 py-1 rounded border border-red-900/50">XYZ-99 DETECTED</span>
                        </div>

                        <div className="overflow-auto custom-scrollbar flex-1 p-2">
                            <table className="w-full text-left border-collapse">
                                <thead>
                                    <tr className="text-[10px] text-slate-500 uppercase tracking-wider border-b border-white/5">
                                        <th className="pb-2 pl-2">Time</th>
                                        <th className="pb-2">Type</th>
                                        <th className="pb-2 text-right">Amount</th>
                                        <th className="pb-2 text-right pr-2">Risk</th>
                                    </tr>
                                </thead>
                                <tbody className="text-xs">
                                    {threats.map((t, i) => (
                                        <tr key={i} className={`border-b border-white/5 hover:bg-white/5 transition font-mono ${t.risk > 0.9 ? 'text-white' : 'text-slate-400'}`}>
                                            <td className="py-3 pl-2">{t.time}</td>
                                            <td className="py-3">
                                                <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${t.risk > 0.9 ? 'bg-red-500/20 text-red-500 neon-text-red' : 'bg-amber-500/20 text-amber-500'}`}>
                                                    {t.type}
                                                </span>
                                            </td>
                                            <td className="py-3 text-right">NPR {(t.amount / 1000).toFixed(1)}k</td>
                                            <td className="py-3 text-right pr-2 font-bold">{t.risk.toFixed(2)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div >

                </div >

            </main >
        </div >
    );
}

// --- SUB-COMPONENTS ---

function KPICard({ label, value, data, color }) {
    return (
        <div className="glass-panel p-3 flex flex-col justify-between rounded relative overflow-hidden group">
            <div className={`absolute top-0 left-0 w-1 h-full bg-[${color}] opacity-50`}></div>
            <div className="flex justify-between items-end mb-2 pl-2">
                <div>
                    <div className="text-[10px] text-slate-500 font-bold">{label}</div>
                    <div className="text-xl font-bold text-white tracking-wider" style={{ textShadow: `0 0 10px ${color}66` }}>{value}</div>
                </div>
            </div>
            <div className="h-8 w-full opacity-50 pl-2">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <Line type="monotone" dataKey="val" stroke={color} strokeWidth={2} dot={false} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

function ToggleSwitch({ label, status }) {
    return (
        <div className="p-3 bg-slate-900/50 border border-white/5 rounded flex flex-col justify-between items-start gap-2">
            <span className="text-[10px] font-bold text-slate-400">{label}</span>
            <div className="flex items-center gap-2">
                <div className={`w-8 h-4 rounded-full p-0.5 flex ${status ? 'bg-emerald-500 justify-end' : 'bg-slate-700 justify-start'}`}>
                    <div className="w-3 h-3 bg-white rounded-full shadow-sm"></div>
                </div>
                <span className="text-xs font-bold text-emerald-400 neon-border-green px-1 rounded">ON</span>
            </div>
        </div>
    )
}

function generateSparklineData(count, min, max) {
    return Array.from({ length: count }, (_, i) => ({
        i, val: Math.floor(min + Math.random() * (max - min))
    }));
}
