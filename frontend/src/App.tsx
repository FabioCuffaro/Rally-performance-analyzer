import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { RallyProvider } from './context/RallyContext'
import { Layout } from './components/Layout'
import { Overview } from './pages/Overview'
import { Stages, Evolution, Compare, Analysis } from './pages/Placeholders'

export default function App() {
  return (
    <RallyProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Overview />} />
            <Route path="stages"    element={<Stages />} />
            <Route path="evolution" element={<Evolution />} />
            <Route path="compare"   element={<Compare />} />
            <Route path="analysis"  element={<Analysis />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </RallyProvider>
  )
}
