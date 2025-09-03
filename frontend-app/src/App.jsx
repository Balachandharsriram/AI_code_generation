import React, { useState } from "react";
import Header from "./components/Header";
import InputForm from "./components/InputForm";
import OutputPanel from "./components/OutputPanel";
import Footer from "./components/Footer";
import jsonToFlow from "./utils/jsonToFlow";

function App() {
  const [description, setDescription] = useState("");
  const [generatedData, setGeneratedData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFormat, setSelectedFormat] = useState("st");

  const generateCode = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/generate_${selectedFormat}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ description }),
        }
      );
      const data = await response.json();
      setGeneratedData(data);
    } catch (error) {
      setGeneratedData({
        error: `Error connecting to server: ${error.message}`,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const { nodes, edges, isJson } =
    generatedData && !generatedData.error ? jsonToFlow(generatedData) : { nodes: [], edges: [], isJson: false };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <div className="h-screen flex flex-col">
        {/* Header - Full width above columns */}
        <div className="p-8 pb-6">
          <Header />
        </div>

        {/* Two-column container - Full height */}
        <div className="flex-1 grid grid-cols-1 xl:grid-cols-2 gap-10 px-8 pb-8">
          {/* Left Column - Input */}
          <div className="bg-gradient-to-br from-gray-800 to-gray-700 p-8 rounded-2xl border border-gray-600 flex flex-col shadow-2xl backdrop-blur-sm">
            <h3 className="text-2xl font-bold text-white mb-8 flex justify-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Input Section
            </h3>
            <div className="flex-1">
              <InputForm
                description={description}
                setDescription={setDescription}
                selectedFormat={selectedFormat}
                setSelectedFormat={setSelectedFormat}
                generateCode={generateCode}
                isLoading={isLoading}
              />
            </div>
          </div>

          {/* Right Column - Output */}
          <div className="bg-gradient-to-br from-gray-800 to-gray-700 p-8 rounded-2xl border border-gray-600 flex flex-col shadow-2xl backdrop-blur-sm">
            <h3 className="text-2xl font-bold text-white mb-8 flex justify-center bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
              Output Section
            </h3>
            <div className="flex-1">
              <OutputPanel
                generatedData={generatedData}
                isJson={isJson}
                selectedFormat={selectedFormat}
                nodes={nodes}
                edges={edges}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;