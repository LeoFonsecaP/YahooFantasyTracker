import standings from './Data/standings/standings.json'
import Apr from './Data/standings/Apr.json'
import Dec from './Data/standings/Dec.json'
import Feb from './Data/standings/Feb.json'
import Jan from './Data/standings/Jan.json'
import Mar from './Data/standings/Mar.json'
import Nov from './Data/standings/Nov.json'
import Oct from './Data/standings/Oct.json'

console.log(Apr)
function Standings(){
    return(
        <div className="standings">
            <div className="standing">
                <h1>Overall</h1>
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
            </div>

            <div className="standing">
                <h1>October</h1>
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
                        Oct.map((team) =>
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
            </div>
            
            <div className="standing">
                <h1>November</h1>
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
                        Nov.map((team) =>
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
            </div>

            <div className="standing">
                <h1>December</h1>
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
                        Dec.map((team) =>
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
            </div>

            <div className="standing">
                <h1>January</h1>
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
                        Jan.map((team) =>
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
            </div>

            <div className="standing">
                <h1>February</h1>
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
                        Feb.map((team) =>
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
            </div>

            <div className="standing">
                <h1>March</h1>
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
                        Mar.map((team) =>
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
            </div>

            <div className="standing">
                <h1>April</h1>
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
                        Apr.map((team) =>
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
            </div>

        </div>
    );
}

export default Standings;