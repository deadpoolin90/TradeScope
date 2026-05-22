import clsx from "clsx";

interface Props {
  label:    string;
  value:    string;
  positive?: boolean;
}

export default function MetricCard({ label, value, positive }: Props) {
  return (
    <div className="space-y-0.5">
      <p className="text-xs text-gray-500">{label}</p>
      <p className={clsx(
        "text-sm font-semibold font-mono",
        positive === true  && "text-profit",
        positive === false && "text-loss",
        positive === undefined && "text-white"
      )}>
        {value}
      </p>
    </div>
  );
}
