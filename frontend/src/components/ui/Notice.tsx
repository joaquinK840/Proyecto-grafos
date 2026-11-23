interface NoticeProps {
  children: string;
  tone?: "error" | "info" | "success";
}

const toneStyles = {
  error: "border-rose-900/80 bg-rose-950/50 text-rose-200",
  info: "border-indigo-900/80 bg-indigo-950/50 text-indigo-200",
  success: "border-emerald-900/80 bg-emerald-950/50 text-emerald-200",
};

/**
 * Colored message box (error, information or success).
 *
 * @param props.children Message; line breaks are preserved.
 * @param props.tone Visual style and ARIA role (errors use role="alert").
 */
export function Notice({ children, tone = "info" }: NoticeProps) {
  return (
    <p
      role={tone === "error" ? "alert" : "status"}
      className={`whitespace-pre-line rounded-xl border px-4 py-3 text-sm ${toneStyles[tone]}`}
    >
      {children}
    </p>
  );
}
