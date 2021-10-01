import standings from './Data/standings/standings.json'
import transactions from './Data/transactions/Transactions.json'
import freeagents from './Data/freeagents/FreeAgents.json'
function Home(){
    return(
        <div className="S1">
        <h1>Mickey Mouse Fantasy - 2021/2022 Season</h1>
        <div className="Season1">
            <table>
                <tr>
                    <th>Rank</th>
                    <th>Logo </th>
                    <th>Team</th>
                    <th>W-L</th>
                    <th>Pct (%)</th>
                    <th>Points</th>
                </tr>
                    {
                        standings.standings.map((team) =>
                        <tr>
                            <td>{team.Rank}</td>
                            <td className="img"><img src={team['Team logo']} width="50px"></img></td>
                            <td className="name">{team.Name}</td>
                            <td>{team.Wins}-{team.Losses}</td>
                            <td>{team.Percentage}</td>
                            <td>{team['Points For']}</td>
                        </tr>
                        )}
            </table>
            <div className = "Categorias">
                <h1>Latest Transactions</h1>
                {transactions.Transactions.slice(0, 5).map((transaction) =>
                        
                        transaction.Players.map((player) =>
                            <li>{player.Name} ({player.Positions}): {player.Source} {'->'} {player.Destination}</li>)
                        )
                }
                <h1>Top Free Agents</h1>
                {
                        freeagents.map((FreeAgent) =>
                        <div className = "freeagents">
                            <li>{FreeAgent.Name} ({FreeAgent.Positions}) - {FreeAgent.Team} </li>
                        </div>
                        )
                }

            </div>
        </div>
    </div>
    );
}

export default Home;