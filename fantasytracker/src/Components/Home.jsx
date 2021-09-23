import week1 from './Data/standings/week1.json'
function Home(){
    return(
        <div className="S1">
        <h1>Mickey Mouse Fantasy - 2021/2022 Season</h1>
        <div className="Season1">
            <table>
                <h2>Current Standings</h2>
                <tr>
                    <th>Rank</th>
                    <th>Team</th>
                    <th>W-L-D</th>
                    <th>Pct (%)</th>
                    <th>Points</th>
                </tr>
                    {
                        week1.standings.map((team) =>
                        <tr>
                            <td>{team.Rank}</td>
                            <td>{team.Name}</td>
                            <td>{team.Wins}-{team.Losses}</td>
                            <td>{team.Percentage}</td>
                            <td>{team['Points For']}</td>
                        </tr>
                        )}
            </table>
            <div className = "Categorias">
                
            </div>
        </div>
    </div>
    );
}

export default Home;