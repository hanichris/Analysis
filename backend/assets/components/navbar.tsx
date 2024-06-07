import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav>
      <ul>
        <li>
          <Link to={""}>
            <img src="/static/analysis/img/logo.svg" alt="logo" />
          </Link>
        </li>
        <div>
          <li>
            <Link to={"about"}>About</Link>
          </li>
          <li>
            <Link to={"contact"}>Contact Us</Link>
          </li>
        </div>
      </ul>
    </nav>
  );
}