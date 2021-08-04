import {
  Switch,
  BrowserRouter as Router,
  Route,
  Redirect,
} from "react-router-dom";
import Header from "./Components/Header";


function App() {
  return (
    <Router>
      <Header />
    </Router>
  );
}

export default App;
