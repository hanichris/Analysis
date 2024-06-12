import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="header">
      <div className="container border-bottom">
        <div className="header-container">
          <div className="header-logo">
            <Link to={""}>
              <img src="/static/analysis/img/logo.svg" alt="logo" width={160} height={140}/>
            </Link>
          </div>
          <input type="checkbox" className="menu-btn" id="menu-btn" />
          <label htmlFor="menu-btn" className="menu-icon">
            <span className="navicon"></span>
          </label>
          <nav className="navbar-menu">
            <ul className="nav">
              <li className="nav-item">
                <Link to={"about"} className="nav-link">About</Link>
              </li>
              <li className="nav-item">
                <Link to={"contact"} className="nav-link">Contact Us</Link>
              </li>
              <li className="nav-item">
                <a href="/accounts/login" className="nav-link">Login</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}