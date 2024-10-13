import './Home.css'

function Home() {
    return(
        <>
        <section className='video-sect'>
            <video autoPlay loop muted playsInline>
                <source src="/Written-Text.mp4" type="video/mp4" />
            </video>
        </section>

        <section className="content-sect">
            <div className="content-wrapper">
                <div className="upload-area">
                    <input type="file" className='file-selector' />
                    <p> Drag and drop a file here, or click to select a file </p>
                </div>

                <div className="text-display">
                    <h2> Generated Text </h2>
                    <p className="output-text"></p>
                </div>
            </div>
        </section>
        </>
    )
}

export default Home
