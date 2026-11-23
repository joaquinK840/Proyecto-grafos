import type { ReactNode } from "react";

interface StatCardProps {
  label: string;
  value: string | number;
  detail: string;
  icon: ReactNode;
  accent?: "indigo" | "cyan" | "emerald" | "amber";
}

const accentStyles = {
  indigo: "bg-indigo-500/10 text-indigo-300 border-indigo-400/10",
  cyan: "bg-cyan-500/10 text-cyan-300 border-cyan-400/10",
  emerald: "bg-emerald-500/10 text-emerald-300 border-emerald-400/10",
  amber: "bg-amber-500/10 text-amber-300 border-amber-400/10",
};

/**
 * Small card with a metric of the dashboard.
 *
 * @param props.label Metric name.
 * @param props.value Main value.
 * @param props.detail Secondary text below the value.
 * @param props.icon Icon shown on the left.
 * @param props.accent Color of the icon box.
 */
export function StatCard({
  label,
  value,
  detail,
  icon,
  accent = "indigo",
}: StatCardProps) {
  return (
    <article className="stat-card">
      <div className={`stat-icon border ${accentStyles[accent]}`}>{icon}</div>
      <div className="min-w-0">
        <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-slate-500">
          {label}
        </p>
        <p className="mt-1 text-2xl font-bold tracking-tight text-white">{value}</p>
        <p className="mt-0.5 truncate text-xs text-slate-400">{detail}</p>
      </div>
    </article>
  );
}
