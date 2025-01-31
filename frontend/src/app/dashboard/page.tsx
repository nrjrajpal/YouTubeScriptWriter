// export default function DashboardPage() {
//     return (
//       <div>
//         <h1>Dashboard</h1>
//         <p>Welcome to your dashboard. Please select a valid project to continue.</p>
//       </div>
//     );
//   }

import DataTableDemo from "@/components/dark-theme-data-table";

export default function Home() {
  return (
    <div className="bg-black flex flex-col items-center pt-14">
      <h1 className="text-4xl font-script font-semibold text-white p-6">Dashboard</h1>
      <DataTableDemo />

    </div>
  );
}

