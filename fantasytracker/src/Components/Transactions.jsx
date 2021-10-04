import transactions from './Data/transactions/Transactions.json'
console.log(transactions.Transactions.length/2)
function Transactions(){
    return(
        <div className="t">
            <div className="transactions">
                <ul>
                {transactions.Transactions.slice(0,transactions.Transactions.length/2).map((transaction) =>
                    transaction.Players.map((player) =>
                        <p>{player.Name} ({player.Positions}): {player.Source} {'->'} {player.Destination}</p>)
                        )}
                </ul>
                <ul>
                {transactions.Transactions.slice(transactions.Transactions.length/2,transactions.Transactions.length).map((transaction) =>
                    transaction.Players.map((player) =>
                        <p>{player.Name} ({player.Positions}): {player.Source} {'->'} {player.Destination}</p>)
                        )}
                </ul>
            </div>
            <p>Last updated: {transactions['Last Updated']}</p>
        </div>
    );
}

export default Transactions;