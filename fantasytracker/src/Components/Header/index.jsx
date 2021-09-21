function Header(){
    return(
        <header>
            <div className = "logo">
            <a Link to = "/">Fantasy Tracker</a>
            </div>
            <ul className = "nav">
                <li><a Link to ="/">Standings</a></li>
                <li><a Link to ="/">Award Race</a></li>
                <li><a Link to ="/">Transactions</a></li>
                <li><a Link to ="/">Previous Seasons</a></li>
                <li><a href ="https://twitter.com" className="fa fa-twitter"></a></li>
            </ul>
        </header>
    );
}

export default Header;