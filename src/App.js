import mainImg from './images/main.png'
import sponsor1 from './images/sponsor1.png'
import daniel from './images/daniel.png'
import wu from './images/wu.png'
import lydia from './images/lydia.png'
import { PrimaryBtn, SecondaryDarkBtn } from './components'

const sponsors = [sponsor1, sponsor1, sponsor1, sponsor1, sponsor1]
const members = ["Dieter Joubert →", "Ritika Deshpande →", "Tanisha Bisht →", "Aaron Zhu →", "Dieter Joubert →", "Aaron Zhu →"]
const publications = [
  {name: 'Playing to Adapt: Crowdsourcing Historical Climate Data with Gamification to Improve Farmer Risk Management Instruments', authors: 'Juan Nicolas Aguilera, Max Mauerman, Daniel Osgood'},
  {name: 'Reptile: Aggregation-level Explanations for Hierarchical Data', authors: 'Zachary Huang, Eugene Wu - SIGMOD 2022'},
  {name: 'Using Tech to Help African Farmers Collect Index Insurance Payouts', authors: 'News Article Aug 2022'},
  {name: 'Voices of CS: Zachary Huang', authors: 'Columbia CS Newsletter'},
  {name: 'In New Project, Millions of Farmers Will Help to Improve Insurance Against Climate Disasters', authors: 'Columbia Climate School newsletter 2021'},
  {name: 'iKON: Playing to Adapt', authors: 'Columbia Climate School newsletter 2021'},
]

function App() {
  return (
    <div className="App">

      <div className='hero'>
        <div className='hero__col_left'>
          <img className='hero__img' src={mainImg} alt='hero' />
        </div>
        <div className='hero__col_right'>
          <h1 className='hero__title'>Open Insurance Toolkit</h1>
          <p className='hero_desc'>Traditional disaster risk management often relies on satellite data, which might not fully reflect the realities faced by vulnerable communities. DESDR (Decision Engine for Socioeconomic Disaster Risk) transforms this approach by integrating firsthand information from those most affected, enhancing accuracy and insight into disaster risks</p>
          <PrimaryBtn onClick={() => console.log('call to action')}>SEE OUR TOOLKIT</PrimaryBtn>
        </div>
      </div>

      <div className='sponsors'>
        {sponsors.map((sponsor,k) => <img key={k} src={sponsor} alt='sponsor' />)}
      </div>

      <div className='toolkit'>
        <h1 className='toolkit__title'>DESDR Toolkit</h1>
        <div className='toolkit__row'>

          <div className='toolkit__col'>
            <div className='div_secondary_light'>01. Survey Your Way →</div>
            <p className='toolkit__subtitle'>DATA COLLECTION</p>
            <p className='toolkit__desc'>Utilizes mobile messaging platforms for accessible and respectful engagement with local communities.</p>
            <div className='div_secondary_light'>Senegal →</div>
          </div>

          <div className='toolkit__col'>
            <div className='div_secondary_light'>02. Reptile →</div>
            <p className='toolkit__subtitle'>DATA VERIFICATION</p>
            <p className='toolkit__desc'>Implements advanced tools to ensure data accuracy and security.</p>
            <div className='div_secondary_light'>Ethiopia →</div>
            <div className='div_secondary_light'>Zambia →</div>
            <div className='div_secondary_light'>Congo →</div>
            <div className='div_secondary_light'>Nigeria →</div>
          </div>

          <div className='toolkit__col'>
            <div className='div_secondary_light'>01. Survey Your Way →</div>
            <p className='toolkit__subtitle'>DATA COLLECTION</p>
            <p className='toolkit__desc'>Utilizes mobile messaging platforms for accessible and respectful engagement with local communities.</p>
            <div className='div_secondary_light'>Ethiopia →</div>
            <div className='div_secondary_light'>Zambia →</div>
            <div className='div_secondary_light'>Nigeria →</div>
          </div>

        </div>
      </div>

      <div className='important'>
        <p className='important_desc'>DESDR will be released as open-source software, free for use by various organizations. This initiative not only aims to improve disaster relief efforts but also empowers the most affected communities by giving them a significant role in the solution-making process.</p>
        <SecondaryDarkBtn>CALL TO ACTION</SecondaryDarkBtn>
      </div>

      <div className='team'>
        <h1>Principal Investigators</h1>
        <div className='team__row'>
          <div className='team__col'>
            <div className='div_secondary_light'>01. Daniel Osgood →</div>
            <img className='team__img' src={daniel} alt='daniel' />
            <p>IRI, Columbia University</p>
          </div>
          <div className='team__col'>
            <div className='div_secondary_light'>02. Eugene Wu →</div>
            <img className='team__img' src={wu} alt='daniel' />
            <p>CS, Columbia University</p>
          </div>
          <div className='team__col'>
            <div className='div_secondary_light'>03. Lydia Chilton →</div>
            <img className='team__img' src={lydia} alt='daniel' />
            <p>CS, Columbia University</p>
          </div>
        </div>
        <h1>Meet our Team</h1>
        <div className='team__grid'>
          {members.map((member,k) => <div key={k} className='div_secondary_light'>{member}</div>)}
        </div>
      </div>

      <div className='publication'>
        <h1 className='publication__title'>Publications</h1>
        {publications.map((publication,k) => <div className='div_secondary_dark'>
          <h3 className='publication__name'>{publication.name}</h3>
          <p className='publication__authors'>{publication.authors}</p>
        </div>)}
      </div>

    </div>
  );
}

export default App;
