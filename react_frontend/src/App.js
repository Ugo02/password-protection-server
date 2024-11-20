import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://server1:5002/api/server1')
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>{data.message}</h1>
      <h2>Data from Server2:</h2>
      {data.data_from_server2.error ? (
        <p>Error: {data.data_from_server2.error}</p>
      ) : (
        <p>{data.data_from_server2.message}</p>
      )}
    </div>
  );
}

export default App;
