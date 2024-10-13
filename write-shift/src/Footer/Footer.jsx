import './Footer.css'

function Footer() {
    const currYear = new Date().getFullYear();

    return(
        <>
        <footer>
            &copy; {currYear}
        </footer>
        </>
    )
}

export default Footer
