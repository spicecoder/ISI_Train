import React, { useState } from 'react';

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
    // Simple boolean logic - either logged in or not
    if (username === validCredentials.username && 
        password === validCredentials.password) {
      setIsLoggedIn(true);
      setError("");
    } else {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="w-80 p-6 border rounded-lg shadow-sm">
      <h2 className="text-xl font-bold mb-4">Traditional Auth</h2>
      {!isLoggedIn ? (
        <div className="space-y-4">
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            className="w-full p-2 border rounded"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full p-2 border rounded"
          />
          <button
            onClick={handleLogin}
            className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Login
          </button>
          {error && <p className="text-red-500 text-sm">{error}</p>}
        </div>
      ) : (
        <p className="text-green-500">Logged in successfully!</p>
      )}
    </div>
  );
};

// PnR Approach Component using Trivalence
const PnRAuth = () => {
  // PnR state with trivalent values
  const [pnrState, setPnrState] = useState({
    credentials: {
      name: "auth_credentials",
      value: ["", "U"]  // U = Undecided/Not yet validated
    },
    validation: {
      name: "auth_validation",
      value: ["", "U"]  // Will be Y/N/U for Valid/Invalid/Checking
    },
    session: {
      name: "auth_session",
      value: ["", "U"]  // Will track session state
    }
  });

  const [formInput, setFormInput] = useState({ username: "", password: "" });

  const handlePnRLogin = () => {
    // First, mark credentials as being checked
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

    // Simulate async validation
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

  return (
    <div className="w-80 p-6 border rounded-lg shadow-sm">
      <h2 className="text-xl font-bold mb-4">PnR Auth</h2>
      <div className="space-y-4">
        <input
          type="text"
          value={formInput.username}
          onChange={(e) => setFormInput(prev => ({ 
            ...prev, 
            username: e.target.value 
          }))}
          placeholder="Username"
          className="w-full p-2 border rounded"
          disabled={pnrState.validation.value[1] === "Y"}
        />
        <input
          type="password"
          value={formInput.password}
          onChange={(e) => setFormInput(prev => ({ 
            ...prev, 
            password: e.target.value 
          }))}
          placeholder="Password"
          className="w-full p-2 border rounded"
          disabled={pnrState.validation.value[1] === "Y"}
        />
        <button
          onClick={handlePnRLogin}
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          disabled={pnrState.validation.value[1] === "Y"}
        >
          Login
        </button>
        <div className="text-sm">
          {pnrState.validation.value[1] === "U" && (
            <p className="text-blue-500">{getStatusMessage()}</p>
          )}
          {pnrState.validation.value[1] === "N" && (
            <p className="text-red-500">{getStatusMessage()}</p>
          )}
          {pnrState.validation.value[1] === "Y" && (
            <p className="text-green-500">{getStatusMessage()}</p>
          )}
        </div>
        
        {/* Debug view of PnR state */}
        <div className="mt-4 p-2 bg-gray-100 rounded text-xs">
          <pre>{JSON.stringify(pnrState, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
};

// Container component to show both approaches
const AuthComparison = () => {
  return (
    <div className="p-8 flex gap-8 flex-wrap">
      <TraditionalAuth />
      <PnRAuth />
    </div>
  );
};

export default AuthComparison;