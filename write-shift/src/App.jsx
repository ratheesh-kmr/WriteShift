import './App.css'

function App() {
    const currYear = new Date().getFullYear();

  return (
    <main>
      <nav>
        <div>
          <h3>WriteShift</h3>
        </div>
      </nav>

      <section className='video-sect'>
        <video autoPlay loop muted playsInline>
          <source src="/Written-Text1.mp4" type="video/mp4" />
        </video>
      </section>

      <section className="content-sect">
        <div className="content-wrapper">
          <div className="upload-area">
            <input type="file" className="hidden" />
            <p>Drag and drop a file here, or click to select a file</p>
          </div>

          <div className="text-display">
            <h2>Generated Text</h2>
            <p className="output-text">.</p>
          </div>
        </div>
      </section>

      <footer>
        <div>
          <p>&copy; {currYear} WriteShift. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}

export default App
