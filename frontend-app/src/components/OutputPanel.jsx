import React, { useState } from "react";
import LadderDiagram from "./LadderDiagram";

function OutputPanel({ generatedData, isJson, selectedFormat, nodes, edges }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const textToCopy = generatedData?.code || generatedData?.error || "Your code will appear here...";
    try {
      await navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  return (
    <div className="w-full space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-100 mb-4">Generated Code</h2>
        {!isJson && (
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-3 py-2 bg-#333A2F hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
            title="Copy to clipboard"
          >
            {copied ? (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Copied!
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Copy
              </>
            )}
          </button>
        )}
      </div>

      {isJson && selectedFormat === "ld" ? (
        <LadderDiagram nodes={nodes} edges={edges} />
      ) : (
        <div className="min-h-[400px] bg-gradient-to-br from-gray-700 to-gray-600 border-2 border-gray-500 rounded-xl overflow-hidden shadow-inner">
          <div 
            className="w-full h-full p-5 text-gray-100 font-mono text-sm leading-relaxed overflow-y-auto output-scroll"
            style={{
              minHeight: '400px',
              maxHeight: '600px'
            }}
          >
            <pre className="whitespace-pre-wrap break-words m-0">
              {generatedData?.code ||
                generatedData?.error ||
                "Your code will appear here..."}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default OutputPanel;