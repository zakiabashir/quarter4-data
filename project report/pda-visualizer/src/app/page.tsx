import Editor from '@/components/Editor/Editor';
import Simulation from '@/components/Simulation/Simulation';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-12 bg-gray-50">
      <h1 className="text-4xl font-bold mb-8">PDA Visualizer</h1>
      <div className="flex w-full max-w-7xl flex-grow gap-8">
        {/* Left side: Editor Panel */}
        <div className="w-1/2 flex flex-col gap-4">
          <h2 className="text-2xl font-semibold">PDA Editor</h2>
          <div className="flex-grow p-4 border rounded-lg bg-white shadow-sm">
            <Editor />
          </div>
        </div>

        {/* Right side: Simulation Panel */}
        <div className="w-1/2 flex flex-col gap-4">
          <h2 className="text-2xl font-semibold">Simulation</h2>
          <div className="flex-grow p-4 border rounded-lg bg-white shadow-sm">
            <Simulation />
          </div>
        </div>
      </div>
    </main>
  );
}
