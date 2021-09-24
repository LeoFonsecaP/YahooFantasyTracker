import {
  Switch,
  BrowserRouter as Router,
  Route,
  Redirect,
} from "react-router-dom";
import Footer from "./Components/footer";
import Header from "./Components/Header";
import PreviousSeasons from "./Components/PreviousSeasons";
import Season1 from "./Components/Season1";
import Season2 from "./Components/Season2";
import Season3 from "./Components/Season3";
import Season4 from "./Components/Season4";
import Season5 from "./Components/Season5";
import History from "./Components/History";
import Home from "./Components/Home";


function App() {
  return (
    <Router>
      <Header />
      <Switch>

        <Route exact path="/">
          <Home />
        </Route>

        <Route path="/PreviousSeasons">
          <PreviousSeasons />
        </Route>
        <Route path="/2021">
          <Season1 />
        </Route>
        <Route path="/2020">
          <Season2 />
        </Route>
        <Route path="/2019">
          <Season3 />
        </Route>
        <Route path="/2018">
          <Season4 />
        </Route>
        <Route path="/2017">
          <Season5 />
        </Route>
        <Route path="/History">
          <History />
        </Route>
        <Route>
          <Redirect to = "/PreviousSeasons" />
        </Route>
      </Switch>
      <Footer />
    </Router>
  );
}

export default App;
