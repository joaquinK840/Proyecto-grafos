import type { ReactNode } from "react";

interface PanelProps {
  title: string;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function Panel({
  title,
  description,
  action,
  children,
  className = "",
}: PanelProps) {
  return (
    <section
      className={`rounded-2xl border border-slate-800 bg-slate-900/80 shadow-xl shadow-black/10 ${className}`}
    >
      <header className="flex items-start justify-between gap-4 border-b border-slate-800 px-5 py-4">
        <div>
          <h2 className="font-semibold text-slate-100">{title}</h2>
          {description && <p className="mt-1 text-sm text-slate-400">{description}</p>}
        </div>
        {action}
      </header>
      <div className="p-5">{children}</div>
    </section>
  );
}
