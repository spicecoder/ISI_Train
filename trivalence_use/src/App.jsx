import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import AuthComparison from './AuthComparion'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
 <AuthComparison/>
    </>
  )
}

export default App
