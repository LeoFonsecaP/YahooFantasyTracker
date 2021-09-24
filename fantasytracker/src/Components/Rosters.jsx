import rosters from './Data/rosters/Rosters.json'
console.log(rosters[0])
//{rosters.map((roster) =>
    //{roster.Name} 
//)}
function Rosters(){
    return(
        <div className="rosters">
                {rosters.map((roster) =>
                    <div className="roster">
                        <img src = {roster['Team logo']}></img>
                        <h3>{roster.Name}</h3>
                        <h3>{roster.Nickname}</h3>
                        {rosters[0].players.map((player) =>
                            <div className="pla">
                                <p>Needs work once draft is done</p>
                                <p>Needs work once draft is done</p>
                                <p>Needs work once draft is done</p>
                                <p>Needs work once draft is done</p>
                                <p>Needs work once draft is done</p>
                                <p>Needs work once draft is done</p>
                                <p>Needs work once draft is done</p>
                                <p>Needs work once draft is done</p>
                            </div>
                        )}
                    </div>
                )}
        </div>
    );
}

export default Rosters;