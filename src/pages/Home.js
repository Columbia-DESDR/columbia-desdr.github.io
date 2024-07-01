import mainImg from '../images/main.png'
import { PrimaryBtn, SecondaryDarkBtn } from '../components'
import {sponsors, toolkit, principalInvestigators, members, publications} from '../constants'
import { useNavigate } from 'react-router-dom';

function App() {

  const navigate = useNavigate();

  return (
    <div className="App">

      <div className='hero'>
        <div className='hero__col_left'>
          <img className='hero__img' src={mainImg} alt='hero' />
        </div>
        <div className='hero__col_right'>
          <h1 className='hero__title'>DESDR</h1>
          <h1 className='hero__title'>Open Insurance Toolkit</h1>
          <p className='hero_desc'>Traditional disaster risk management often relies on satellite data, which might not fully reflect the realities faced by vulnerable communities. DESDR (Decision Engine for Socioeconomic Disaster Risk) transforms this approach by integrating firsthand information from those most affected, enhancing accuracy and insight into disaster risks</p>
          <PrimaryBtn onClick={() => console.log('call to action')} id={'#toolkit-section'}>EXPLORE OUR TOOLKIT</PrimaryBtn>
        </div>
      </div>

      <div className='sponsors'>
        {sponsors.map((sponsor,k) => <img key={k} src={sponsor} alt='sponsor' />)}
      </div>

      <div className='toolkit' id='toolkit-section'>
        <h1 className='toolkit__title'>DESDR Toolkit</h1>
        <div className='toolkit__row'>

          {toolkit.map((tool,ki) => (
            <div className='toolkit__col' key={ki}>
              <div onClick={() => navigate(tool.link)} className='div_secondary_light'>{tool.name}</div>
              <p className='toolkit__subtitle'>{tool.subName}</p>
              <p className='toolkit__desc'>{tool.desc}</p>
              {tool.deployed.map((dep,kj) => (
                <div onClick={() => window.open(dep.link, '_blank')} className='div_secondary_light' key={kj}>{dep.name}</div>
              ))}
            </div>
          ))}

        </div>
      </div>

      <div className='important'>
        <p className='important_desc'>DESDR will be released as open-source software, free for use by various organizations. This initiative not only aims to improve disaster relief efforts but also empowers the most affected communities by giving them a significant role in the solution-making process.</p>
        <SecondaryDarkBtn onClick={() => window.open('https://github.com/Columbia-DESDR', '_blank')}>VISIT OUR REPOSITORY</SecondaryDarkBtn>
      </div>

      <div className='team'>
        <h1>Principal Investigators</h1>
        <div className='team__row'>
          {principalInvestigators.map((mem,k) => <div key={k} className='team__col' onClick={() => window.open(mem.link, '_blank')}>
            <div className='div_secondary_light'>{mem.name}</div>
            <img className='team__img' src={mem.img} alt={mem.name} />
            <p>{mem.college}</p>
          </div>)}
        </div>

        <h1>Meet our Team</h1>
        <div className='team__grid'>
          {members.map((member,k) => <div key={k} className='div_secondary_light'>{member}</div>)}
        </div>
      </div>

      <div className='publication'>
        <h1 className='publication__title'>Publications</h1>
        {publications.map((publication,k) => <div className='div_secondary_dark' onClick={() => window.open(publication.link, '_blank')}>
          <h3 className='publication__name'>{publication.name}</h3>
          <p className='publication__authors'>{publication.authors}</p>
        </div>)}
      </div>

    </div>
  );
}

export default App;