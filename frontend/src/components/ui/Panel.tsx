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
      className={`panel ${className}`}
    >
      <header className="panel-header">
        <div>
          <h2 className="text-[15px] font-semibold text-slate-100">{title}</h2>
          {description && <p className="mt-1 text-xs leading-5 text-slate-400">{description}</p>}
        </div>
        {action}
      </header>
      <div className="p-5">{children}</div>
    </section>
  );
}
