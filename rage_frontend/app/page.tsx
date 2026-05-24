"use client";

import { useState } from "react";

export default function Home() {

  const [file, setFile] = useState<File | null>(null);

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [contexts, setContexts] = useState<any[]>([]);



  const uploadPDF = async () => {

    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
      "http://localhost:8000/upload-pdf",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    console.log(data);

    alert("PDF uploaded successfully!");
  };



  const askQuestion = async () => {

    const response = await fetch(
      "http://localhost:8000/ask",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          question: question,
        }),
      }
    );

    const data = await response.json();

    console.log(data);

    setAnswer(data.answer);

    setContexts(data.retrieved_context);
  };



  return (
    <main className="min-h-screen bg-black text-white p-8">

      <h1 className="text-4xl font-bold mb-8">
        RAGe Against The Machine
      </h1>



      <div className="border border-gray-700 rounded-xl p-6 mb-8">

        <h2 className="text-2xl mb-4">
          Upload PDF
        </h2>

       <div className="mb-4">

  <input
    type="file"
    accept=".pdf"
    onChange={(e) => {
      if (e.target.files) {
        setFile(e.target.files[0]);
      }
    }}
    className="
      block
      w-full
      text-sm
      text-gray-300
      border
      border-gray-700
      rounded-lg
      cursor-pointer
      bg-gray-900
      focus:outline-none
      p-2
    "
  />

  {file && (
    <p className="mt-2 text-green-400 text-sm">
      Selected: {file.name}
    </p>
  )}

</div>

        <br />

        <button
          onClick={uploadPDF}
          className="bg-white text-black px-4 py-2 rounded-lg"
        >
          Upload
        </button>

      </div>



      <div className="border border-gray-700 rounded-xl p-6">

        <h2 className="text-2xl mb-4">
          Ask Question
        </h2>

        <input
          type="text"
          placeholder="Ask something about your PDFs..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full p-3 rounded-lg bg-gray-900 border border-gray-700 mb-4"
        />

        <button
          onClick={askQuestion}
          className="bg-green-500 text-black px-4 py-2 rounded-lg"
        >
          Ask
        </button>



        {answer && (

          <div className="mt-8">

            <h3 className="text-xl font-bold mb-2">
              Answer
            </h3>

            <div className="bg-gray-900 p-4 rounded-lg whitespace-pre-wrap">
              {answer}
            </div>

          </div>
        )}



        {contexts.length > 0 && (

          <div className="mt-8">

            <h3 className="text-xl font-bold mb-4">
              Retrieved Context
            </h3>

            {contexts.map((ctx, index) => (

              <div
                key={index}
                className="bg-gray-900 p-4 rounded-lg mb-4"
              >

                <p>
                  <strong>Document:</strong> {ctx.document_name}
                </p>

                <p>
                  <strong>Page:</strong> {ctx.page_number}
                </p>

                <p>
                  <strong>Chunk:</strong> {ctx.chunk_index}
                </p>

                <hr className="my-2 border-gray-700" />

                <p className="whitespace-pre-wrap">
                  {ctx.content}
                </p>

              </div>
            ))}

          </div>
        )}

      </div>

    </main>
  );
}