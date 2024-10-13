import './App.css'
import Home from './components/Home/Home';

function App() {
    const currYear = new Date().getFullYear();

  return (
    <main>
      <nav>
        <h3> WriteShift </h3>
      </nav>

      <Home />

      <footer>
        &copy; {currYear} WriteShift. All rights reserved.
      </footer>
    </main>
  )
}

export default App
