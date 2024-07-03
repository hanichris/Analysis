import { Link } from "react-router-dom";

import SignInSignUp from "./modal";
import { useState } from "react";

export default function Navbar() {
  const [toggle, setToggle] = useState(false);

  const handleClick = () => setToggle((toggle) => !toggle);

  return (
    <>
      <header className="header">
        <div className="container border-bottom">
          <div className="header-container">
            <div className="header-logo">
              <Link to={""}>
                <img src="/static/analysis/img/logo.svg" alt="logo" width={90} height={90}/>
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
                  <a role="button" className="nav-link" onClick={handleClick}>Login</a>
                </li>
                <li className="nav-item">
                  <a
                    href="https://divergentag.lemonsqueezy.com/buy/d7a1de19-73f5-4873-bc91-b8633c5b4a54"
                    className="nav-link">
                      Pricing
                  </a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </header>
      <SignInSignUp toggle={toggle} setToggle={handleClick}/>
    </>
  );
}