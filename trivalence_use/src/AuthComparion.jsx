import React, { useState } from 'react';

// Simple styled components using template literals
const Container = ({ children }) => (
  <div style={{
    padding: '2rem',
    display: 'flex',
    gap: '2rem',
    flexWrap: 'wrap',
    fontFamily: 'system-ui, sans-serif'
  }}>
    {children}
  </div>
);

const AuthCard = ({ children }) => (
  <div style={{
    width: '320px',
    padding: '1.5rem',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    backgroundColor: 'white',
    border: '1px solid #e5e7eb'
  }}>
    {children}
  </div>
);

const Title = ({ children }) => (
  <h2 style={{
    fontSize: '1.25rem',
    fontWeight: '600',
    marginBottom: '1.5rem',
    color: '#1f2937'
  }}>
    {children}
  </h2>
);

const Input = ({ ...props }) => (
  <input
    style={{
      width: '100%',
      padding: '0.75rem',
      marginBottom: '1rem',
      borderRadius: '6px',
      border: '1px solid #d1d5db',
      fontSize: '0.875rem',
      outline: 'none',
      transition: 'border-color 0.2s',
      ':focus': {
        borderColor: '#3b82f6'
      }
    }}
    {...props}
  />
);

const Button = ({ children, ...props }) => (
  <button
    style={{
      width: '100%',
      padding: '0.75rem',
      backgroundColor: '#3b82f6',
      color: 'white',
      border: 'none',
      borderRadius: '6px',
      fontSize: '0.875rem',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'background-color 0.2s',
      ':hover': {
        backgroundColor: '#2563eb'
      },
      ':disabled': {
        backgroundColor: '#93c5fd',
        cursor: 'not-allowed'
      }
    }}
    {...props}
  >
    {children}
  </button>
);

const Message = ({ type, children }) => {
  const colors = {
    error: '#ef4444',
    success: '#10b981',
    info: '#3b82f6'
  };

  return (
    <p style={{
      fontSize: '0.875rem',
      color: colors[type] || '#6b7280',
      marginTop: '0.75rem'
    }}>
      {children}
    </p>
  );
};

const DebugView = ({ data }) => (
  <pre style={{
    marginTop: '1rem',
    padding: '0.75rem',
    backgroundColor: '#f3f4f6',
    borderRadius: '6px',
    fontSize: '0.75rem',
    overflowX: 'auto'
  }}>
    {JSON.stringify(data, null, 2)}
  </pre>
);

// Mock credentials for demo
const validCredentials = {
  username: "demo",
  password: "password123"
};

// Traditional Boolean Approach Component
const TraditionalAuth = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = () => {
    if (username === validCredentials.username && 
        password === validCredentials.password) {
      setIsLoggedIn(true);
      setError("");
    } else {
      setError("Invalid credentials");
    }
  };

  return (
    <AuthCard>
      <Title>Traditional Auth</Title>
      {!isLoggedIn ? (
        <>
          <Input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
          />
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
          <Button onClick={handleLogin}>Login</Button>
          {error && <Message type="error">{error}</Message>}
        </>
      ) : (
        <Message type="success">Logged in successfully!</Message>
      )}
    </AuthCard>
  );
};

// PnR Approach Component using Trivalence
const PnRAuth = () => {
  const [pnrState, setPnrState] = useState({
    credentials: {
      name: "auth_credentials",
      value: ["", "U"]
    },
    validation: {
      name: "auth_validation",
      value: ["", "U"]
    },
    session: {
      name: "auth_session",
      value: ["", "U"]
    }
  });

  const [formInput, setFormInput] = useState({ username: "", password: "" });

  const handlePnRLogin = () => {
    setPnrState(prev => ({
      ...prev,
      credentials: {
        ...prev.credentials,
        value: [JSON.stringify(formInput), "U"]
      },
      validation: {
        ...prev.validation,
        value: ["checking", "U"]
      }
    }));

    setTimeout(() => {
      if (formInput.username === validCredentials.username && 
          formInput.password === validCredentials.password) {
        setPnrState(prev => ({
          credentials: {
            ...prev.credentials,
            value: [JSON.stringify(formInput), "Y"]
          },
          validation: {
            ...prev.validation,
            value: ["valid", "Y"]
          },
          session: {
            ...prev.session,
            value: ["active", "Y"]
          }
        }));
      } else {
        setPnrState(prev => ({
          ...prev,
          credentials: {
            ...prev.credentials,
            value: [JSON.stringify(formInput), "N"]
          },
          validation: {
            ...prev.validation,
            value: ["invalid", "N"]
          }
        }));
      }
    }, 1000);
  };

  const getStatusMessage = () => {
    const { validation, session } = pnrState;
    if (validation.value[1] === "U") return "Checking credentials...";
    if (validation.value[1] === "N") return "Invalid credentials";
    if (validation.value[1] === "Y" && session.value[1] === "Y") 
      return "Logged in successfully!";
    return "";
  };

  const getMessageType = () => {
    const { validation } = pnrState;
    if (validation.value[1] === "U") return "info";
    if (validation.value[1] === "N") return "error";
    return "success";
  };

  return (
    <AuthCard>
      <Title>PnR Auth</Title>
      <Input
        type="text"
        value={formInput.username}
        onChange={(e) => setFormInput(prev => ({ 
          ...prev, 
          username: e.target.value 
        }))}
        placeholder="Username"
        disabled={pnrState.validation.value[1] === "Y"}
      />
      <Input
        type="password"
        value={formInput.password}
        onChange={(e) => setFormInput(prev => ({ 
          ...prev, 
          password: e.target.value 
        }))}
        placeholder="Password"
        disabled={pnrState.validation.value[1] === "Y"}
      />
      <Button
        onClick={handlePnRLogin}
        disabled={pnrState.validation.value[1] === "Y"}
      >
        Login
      </Button>
      
      {getStatusMessage() && (
        <Message type={getMessageType()}>
          {getStatusMessage()}
        </Message>
      )}
      
      <DebugView data={pnrState} />
    </AuthCard>
  );
};

// Main component
const AuthComparison = () => {
  return (
    <Container>
      <TraditionalAuth />
      <PnRAuth />
    </Container>
  );
};

export default AuthComparison;