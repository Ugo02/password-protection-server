import React, { useState } from 'react';

function App() {
  const [view, setView] = useState('home'); // 'home', 'login', or 'signup'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [responseMessage, setResponseMessage] = useState(null);
  const [entropyMessage, setEntropyMessage] = useState(null);

  const containerStyle = {
    fontFamily: 'Roboto, sans-serif',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    minHeight: '100vh',
    background: '#f3f4f6',
    padding: '20px',
  };

  const cardStyle = {
    background: '#fff',
    borderRadius: '8px',
    padding: '30px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
    maxWidth: '400px',
    width: '100%',
    boxSizing: 'border-box',
    marginBottom: '20px',
  };

  const titleStyle = {
    fontSize: '1.5rem',
    fontWeight: '700',
    marginBottom: '20px',
    color: '#1f2937',
  };

  const labelStyle = {
    display: 'block',
    marginBottom: '5px',
    fontWeight: '500',
    color: '#4b5563',
  };

  const inputStyle = {
    width: '100%',
    padding: '10px',
    marginBottom: '15px',
    borderRadius: '5px',
    border: '1px solid #d1d5db',
    fontSize: '1rem',
    fontFamily: 'inherit',
    outline: 'none',
    color: '#374151',
  };

  const buttonContainerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    marginTop: '20px',
  };

  const buttonStyle = {
    padding: '10px 15px',
    background: '#3b82f6',
    border: 'none',
    borderRadius: '5px',
    color: '#fff',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'background 0.3s',
    fontSize: '1rem',
  };

  const secondaryButtonStyle = {
    ...buttonStyle,
    background: '#6b7280',
  };

  const messageWrapperStyle = {
    maxWidth: '400px',
    width: '100%',
    boxSizing: 'border-box',
  };

  const errorStyle = {
    marginTop: '20px',
    padding: '10px',
    borderRadius: '5px',
    background: '#fee2e2',
    color: '#b91c1c',
  };

  const successStyle = {
    marginTop: '20px',
    padding: '10px',
    borderRadius: '5px',
    background: '#d1fae5',
    color: '#065f46',
  };

  // Function to calculate password entropy
  const calculatePasswordEntropy = (password) => {
    const characterSets = [
      { regex: /[a-z]/, count: 26 }, // Lowercase letters
      { regex: /[A-Z]/, count: 26 }, // Uppercase letters
      { regex: /[0-9]/, count: 10 }, // Numbers
      { regex: /[!@#$%^&*(),.?":{}|<>]/, count: 33 }, // Special characters
    ];

    let N = 0;
    characterSets.forEach((set) => {
      if (set.regex.test(password)) {
        N += set.count;
      }
    });

    const L = password.length;
    const entropy = L > 0 ? (L * Math.log2(N)) : 0;
    return entropy;
  };

  const handlePasswordInput = (e) => {
    const inputPassword = e.target.value;
    setPassword(inputPassword);

    const entropy = calculatePasswordEntropy(inputPassword);
    if (entropy >= 64) {
      setEntropyMessage({ message: `Good password entropy (${Math.round(entropy)} bits)`, isGood: true });
    } else {
      setEntropyMessage({ message: `Password too weak (${Math.round(entropy)} bits). Consider making it stronger.`, isGood: false });
    }
  };

  const handleSignUpRequest = () => {
    if (!username || !password || !confirmPassword) {
      alert("Please fill in all fields.");
      return;
    }
    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    if (entropyMessage && !entropyMessage.isGood) {
      alert("Your password does not meet entropy requirements. Please make it stronger.");
      return;
    }

    const url = 'http://localhost:5002/api/hash_password';

    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log('Sign Up Server response:', data);
        setResponseMessage(data);
      })
      .catch((err) => {
        console.error('Error:', err);
        setResponseMessage({ error: 'Failed to sign up' });
      });
  };

  const handleLoginRequest = () => {
    if (!username || !password) {
      alert("Please fill in both username and password.");
      return;
    }

    const url = 'http://localhost:5002/api/login';

    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log('Login Server response:', data);
        setResponseMessage(data);
      })
      .catch((err) => {
        console.error('Error:', err);
        setResponseMessage({ error: 'Failed to login' });
      });
  };

  const renderHome = () => (
    <div style={cardStyle}>
      <h1 style={titleStyle}>Welcome to our Symmetric Key Project</h1>
      <p style={{ color: '#6b7280', marginBottom: '30px' }}>by Ugo Monneau and Pierre Hohl</p>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <button
          style={buttonStyle}
          onClick={() => {
            setView('signup');
            setResponseMessage(null);
          }}
        >
          Sign Up
        </button>
        <button
          style={secondaryButtonStyle}
          onClick={() => {
            setView('login');
            setResponseMessage(null);
          }}
        >
          Login
        </button>
      </div>
    </div>
  );

  const renderSignUp = () => (
    <div style={cardStyle}>
      <h1 style={titleStyle}>Sign Up</h1>
      <label style={labelStyle}>Username:</label>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={inputStyle}
      />

      <label style={labelStyle}>Password:</label>
      <input
        type="password"
        value={password}
        onChange={handlePasswordInput}
        style={inputStyle}
      />

      <label style={labelStyle}>Confirm Password:</label>
      <input
        type="password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        style={inputStyle}
      />

      {entropyMessage && (
        <div style={entropyMessage.isGood ? successStyle : errorStyle}>
          {entropyMessage.message}
        </div>
      )}

      <div style={buttonContainerStyle}>
        <button onClick={handleSignUpRequest} style={buttonStyle}>
          Sign Up
        </button>
        <button onClick={() => setView('home')} style={secondaryButtonStyle}>
          Back
        </button>
      </div>
    </div>
  );

  const renderLogin = () => (
    <div style={cardStyle}>
      <h1 style={titleStyle}>Login</h1>
      <label style={labelStyle}>Username:</label>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={inputStyle}
      />

      <label style={labelStyle}>Password:</label>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={inputStyle}
      />

      <div style={buttonContainerStyle}>
        <button onClick={handleLoginRequest} style={buttonStyle}>
          Login
        </button>
        <button onClick={() => setView('home')} style={secondaryButtonStyle}>
          Back
        </button>
      </div>
    </div>
  );

  const renderResponse = () => {
    if (!responseMessage) return null;

    // If there is an error, show red
    if (responseMessage.error) {
      return (
        <div style={messageWrapperStyle}>
          <div style={errorStyle}>Error: {responseMessage.error}</div>
        </div>
      );
    }

    // If there's a message and it includes "failed", treat it as an error
    if (responseMessage.message && responseMessage.message.toLowerCase().includes('failed')) {
      return (
        <div style={messageWrapperStyle}>
          <div style={errorStyle}>{responseMessage.message}</div>
        </div>
      );
    }

    // Otherwise, treat as success
    return (
      <div style={messageWrapperStyle}>
        {responseMessage.message && <div style={successStyle}>{responseMessage.message}</div>}
      </div>
    );
  };

  return (
    <div style={containerStyle}>
      {view === 'home' && renderHome()}
      {view === 'signup' && renderSignUp()}
      {view === 'login' && renderLogin()}

      {renderResponse()}
    </div>
  );
}

export default App;
