function Header(){

    return(
        <header>
            <div className = "logo">
            <a Link to = "/">Fantasy Tracker</a>
            </div>
            <ul className = "nav">
                <li><a Link to ="/">Classificação</a></li>
                <li><a Link to ="/">Prêmios</a></li>
                <li><a Link to ="/">Jogadores</a></li>
            </ul>
        </header>
    );
}

export default Header;