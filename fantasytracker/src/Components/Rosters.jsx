import rosters from './Data/rosters/Rosters.json'
console.log(rosters)
function Rosters(){
    return(
        <div className="rosters">
                {rosters.map((roster) =>
                    <div className="roster">
                        <img src = {roster['Team logo']}></img>
                        <h3>{roster.Name}</h3>
                        <h3>{roster.Nickname}</h3>
                        {roster.players.map((player) =>
                            <div className="play">
                                <p><b>{player.Name} ({player.Positions}) </b>- {player.Team}</p>
                            </div>
                        )}
                    </div>
                )}
        </div>
    );
}

export default Rosters;