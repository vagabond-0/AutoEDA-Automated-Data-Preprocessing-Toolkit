import React from "react";

const ScrollableCard = ({ data }) => {
  
  if (!data) {
    return <div>No summary available yet.</div>;
  }

  // Destructure the values from the data object.
  const { filename, status, summary } = data;

  return (
    <div className="overflow-y-auto h-full p-4">
      <h2 className="text-lg font-bold mb-2">File uploaded successfully</h2>
      <p>
        <strong>Filename:</strong> {filename}
      </p>
      <p>
        <strong>Status:</strong> {status}
      </p>
      <div className="mt-4">
        <h3 className="text-md font-semibold mb-1">Summary</h3>
        
        {/* show the entire summary object pretty-printed */}
        {/* <pre className="text-sm dark:bg-gray-800 bg-gray-200 p-2 rounded">
          {JSON.stringify(summary, null, 2)}
        </pre> */}

        {/* render parts of the summary separately */}
        {summary && (
          <>
            <h4>Categorical Columns</h4>
            <pre>{JSON.stringify(summary["Categorical Columns"], null, 2)}</pre>
            <h4>Numerical Columns</h4>
            <pre>{JSON.stringify(summary["Numerical Columns"], null, 2)}</pre>
          </>
        )} 
       
      </div>
    </div>
  );
};

export default ScrollableCard;
