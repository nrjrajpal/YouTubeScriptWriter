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
      <div className="bg-gray-900 flex flex-col items-center">
        <h1 className="text-5xl font-bold text-white p-6">Dashboard</h1>
        <DataTableDemo/>
        
      </div>
    );
  }
  
  