import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Home, SurveyYourWay, Reptile, Sliders } from './pages'

function App() {
  return (
  <Router>
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/survey-your-way" element={<SurveyYourWay />} />
        <Route path="/reptile" element={<Reptile />} />
        <Route path="/sliders" element={<Sliders />} />
      </Routes>
    </div>
  </Router>
  );
}

export default App;
