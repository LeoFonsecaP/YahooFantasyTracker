import React, {useState} from "react";
import { Link } from "react-router-dom";

function Header(){
    const [isActive, setActive] = useState(false);
    return(
        <header>
            <div className = "logo">
            <Link to = "/" onClick={() => setActive(false)}>Fantasy Tracker</Link>
            </div>
            <ul className = "nav">
                <li><Link to ="/Rosters">Rosters</Link></li>
                <li><Link to ="/Standings">Standings</Link></li>
                <li><Link to ="/Transactions">Transactions</Link></li>
                <li><Link to ="/PreviousSeasons">Previous Seasons</Link></li>
            </ul>
            <div className="icons">
                <a href ="https://twitter.com/JowNPSE" target="_blank" className="fa fa-twitter"></a>
                <button className="fa fa-bars menu" onClick={() => setActive(true)}></button>
            </div>
            {isActive &&
                <ul className = "navmobile">
                   <li><Link to ="/Rosters" onClick={() => setActive(false)}>Rosters</Link></li>
                   <li><Link to ="/Standings" onClick={() => setActive(false)}>Standings</Link></li>
                    <li><Link to ="/Transactions" onClick={() => setActive(false)}>Transactions</Link></li>
                    <li><Link to ="/PreviousSeasons" onClick={() => setActive(false)}>Previous Seasons</Link></li>
                    <li><button onClick={() => setActive(false)}> Fechar</button></li>
                </ul>
            }
        </header>
    );
}

export default Header;