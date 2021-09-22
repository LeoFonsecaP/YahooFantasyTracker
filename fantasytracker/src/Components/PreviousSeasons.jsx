import { Link } from "react-router-dom";

function PreviousSeasons(){
    return(
        <ul className="PrevSeasons">
            <li><Link to="/2021">Ano passado não valeu - 2020/2021 Season</Link></li>
            <li><Link to="/2020">Ninguém torce pra contender - 2019/2020 Season*</Link></li>
            <li><Link to="/2019">Cousins é um cuzao - 2018/2019 Season</Link></li>
            <li><Link to="/2018">O Leo fala muita merda - 2017/2018 Season</Link></li>
            <li><Link to="/2017">Curry é só um molho - 2016/2017 Season</Link></li>
            <li><Link to="/History">History</Link></li>
        </ul>
    );
}

export default PreviousSeasons;