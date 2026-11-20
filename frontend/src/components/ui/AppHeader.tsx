import { Activity, GitBranch, RefreshCw } from "lucide-react";

interface AppHeaderProps {
  isLoading: boolean;
  onRefresh: () => void;
}

export function AppHeader({ isLoading, onRefresh }: AppHeaderProps) {
  return (
    <header className="flex flex-col gap-5 border-b border-slate-800/80 pb-6 lg:flex-row lg:items-end lg:justify-between">
      <div className="flex items-center gap-4">
        <div className="brand-mark">
          <GitBranch size={27} strokeWidth={2} />
        </div>
        <div>
          <div className="mb-1 flex items-center gap-2">
            <span className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.18em] text-cyan-300">
              Proyecto SismoLab
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white sm:text-[2rem]">
            Centro de operaciones
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Defensa del corredor · Grafos GE y GM
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className="hidden items-center gap-2 rounded-xl border border-slate-800 bg-slate-950/50 px-3 py-2 text-xs text-slate-400 sm:flex">
          <Activity size={14} className="text-emerald-400" />
          Sistema en línea
        </div>
        <button
          type="button"
          onClick={onRefresh}
          disabled={isLoading}
          className="button-secondary"
        >
          <RefreshCw size={15} className={isLoading ? "animate-spin" : ""} />
          Actualizar
        </button>
      </div>
    </header>
  );
}
