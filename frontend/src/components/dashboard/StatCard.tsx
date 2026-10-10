interface StatCardProps {
  title: string;
  value: string;
}

export default function StatCard({
  title,
  value,
}: StatCardProps) {
  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <h2 className="text-sm text-gray-600">
        {title}
      </h2>

      <p className="mt-3 text-3xl font-bold">
        {value}
      </p>
    </div>
  );
}