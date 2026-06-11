import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { RallyProvider } from './context/RallyContext'
import { Layout } from './components/Layout'
import { Overview } from './pages/Overview'
import { Stages } from './pages/Stages'
import { Evolution } from './pages/Evolution'
import { Compare } from './pages/Compare'
import { Analysis } from './pages/Analysis'
import { Season } from './pages/Season'

export default function App() {
  return (
    <RallyProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index              element={<Overview />}   />
            <Route path="stages"      element={<Stages />}     />
            <Route path="evolution"   element={<Evolution />}  />
            <Route path="compare"     element={<Compare />}    />
            <Route path="analysis"    element={<Analysis />}   />
            <Route path="season"      element={<Season />}     />
          </Route>
        </Routes>
      </BrowserRouter>
    </RallyProvider>
  )
}
