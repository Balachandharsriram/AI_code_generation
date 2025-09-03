import React from "react";

function InputForm({ description, setDescription, selectedFormat, setSelectedFormat, generateCode, isLoading }) {
  return (
    <div className="w-full space-y-6">
      <div>
        <label
          htmlFor="format-select"
          className="block text-gray-100 font-semibold mb-3 text-lg"
        >
          Choose Output Format:
        </label>
        <select
          id="format-select"
          value={selectedFormat}
          onChange={(e) => setSelectedFormat(e.target.value)}
          className="w-full p-4 border-2 border-gray-500 bg-gray-700 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all duration-200 hover:border-gray-400"
        >
          <option value="st">Structured Text</option>
          <option value="ld">Ladder Diagram (Visual)</option>
        </select>
      </div>

      <div>
        <label className="block text-gray-100 font-semibold mb-3 text-lg">
          Description:
        </label>
        <textarea
          className="w-full h-48 p-4 border-2 border-gray-500 bg-gray-700 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all duration-200 hover:border-gray-400 resize-none"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g., When the start button is pressed, turn on motor 1 for 10 seconds."
        />
      </div>

      <div className="flex justify-center pt-4">
        <button
          className="px-12 py-4 font-bold text-lg text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-105"
          onClick={generateCode}
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Generate Code"}
        </button>
      </div>
    </div>
  );
}

export default InputForm;
