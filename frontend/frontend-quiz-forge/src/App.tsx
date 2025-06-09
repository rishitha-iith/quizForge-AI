import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import QuizPage from './pages/QuizPage';
import ResultPage from './pages/ResultPage';
import NavBar from './components/NavBar';

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz/:userId" element={<QuizPage />} />
        <Route path="/result/:userId" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
